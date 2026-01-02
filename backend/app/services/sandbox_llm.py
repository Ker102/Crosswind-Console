"""
Sandbox LLM Service - Combines RAG context with Remote MCP tool calling
"""
import asyncio
import os
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

try:
    import google.generativeai as genai
except ImportError:
    genai = None

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from .rag_service import RAGService


@dataclass
class SandboxResult:
    text: str
    latency_ms: float
    model: str
    tools_used: List[str]
    rag_context: List[Dict]


# Remote MCP Server configurations
REMOTE_MCP_SERVERS = {
    "rapidapi-sky": {
        "command": "npx",
        "args": ["-y", "mcp-remote", "https://mcp.rapidapi.com",
                 "--header", f"x-api-host: flights-sky.p.rapidapi.com",
                 "--header", f"x-api-key: {os.getenv('RAPIDAPI_KEY', '')}"],
        "category": "travel"
    },
    "rapidapi-booking": {
        "command": "npx",
        "args": ["-y", "mcp-remote", "https://mcp.rapidapi.com",
                 "--header", f"x-api-host: booking-com.p.rapidapi.com", 
                 "--header", f"x-api-key: {os.getenv('RAPIDAPI_KEY', '')}"],
        "category": "travel"
    },
    "google-maps": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-google-maps"],
        "env": {"GOOGLE_MAPS_API_KEY": os.getenv("GOOGLE_MAPS_API_KEY", "")},
        "category": "travel"
    }
}


class SandboxLLMService:
    """LLM service for Sandbox mode with RAG + Remote MCP"""
    
    def __init__(self, gemini_api_key: str, model_id: str = "gemini-2.0-flash"):
        self.model_id = model_id
        self._api_key = gemini_api_key
        self._enabled = bool(gemini_api_key and genai)
        self._model = None
        self.rag_service = RAGService()
        self._tool_cache: Dict[str, List] = {}  # Cache discovered tools
        
        if self._enabled:
            genai.configure(api_key=gemini_api_key)
            self._model = genai.GenerativeModel(
                model_id,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=8192
                )
            )
    
    async def _get_remote_tools(self, server_name: str) -> List[Dict]:
        """Fetch tools from a remote MCP server"""
        if server_name in self._tool_cache:
            return self._tool_cache[server_name]
        
        config = REMOTE_MCP_SERVERS.get(server_name)
        if not config:
            return []
        
        env = {**os.environ}
        if "env" in config:
            env.update(config["env"])
        
        server_params = StdioServerParameters(
            command=config["command"],
            args=config["args"],
            env=env
        )
        
        tools = []
        try:
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    result = await session.list_tools()
                    for tool in result.tools:
                        tools.append({
                            "name": tool.name,
                            "description": tool.description,
                            "inputSchema": tool.inputSchema,
                            "server": server_name
                        })
        except Exception as e:
            print(f"Error fetching tools from {server_name}: {e}")
        
        self._tool_cache[server_name] = tools
        return tools
    
    async def _call_remote_tool(self, server_name: str, tool_name: str, arguments: Dict) -> str:
        """Execute a tool on a remote MCP server"""
        config = REMOTE_MCP_SERVERS.get(server_name)
        if not config:
            return f"Error: Server '{server_name}' not found"
        
        env = {**os.environ}
        if "env" in config:
            env.update(config["env"])
        
        server_params = StdioServerParameters(
            command=config["command"],
            args=config["args"],
            env=env
        )
        
        try:
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    result = await session.call_tool(tool_name, arguments)
                    
                    # Extract text from result
                    texts = []
                    for item in result.content:
                        if hasattr(item, 'text'):
                            texts.append(item.text)
                    return "\n".join(texts) if texts else str(result)
        except Exception as e:
            return f"Error calling {tool_name}: {e}"
    
    def _build_gemini_tools(self, mcp_tools: List[Dict]) -> List:
        """Convert MCP tool schemas to Gemini FunctionDeclaration format"""
        declarations = []
        
        for tool in mcp_tools:
            if not tool.get("inputSchema"):
                continue
            
            # Convert JSON Schema to Gemini format
            properties = {}
            required = tool["inputSchema"].get("required", [])
            
            for prop_name, prop_def in tool["inputSchema"].get("properties", {}).items():
                prop_type = prop_def.get("type", "string")
                
                # Map JSON Schema types to Gemini types
                type_map = {
                    "string": "STRING",
                    "number": "NUMBER",
                    "integer": "INTEGER",
                    "boolean": "BOOLEAN",
                    "array": "ARRAY",
                    "object": "OBJECT"
                }
                
                properties[prop_name] = {
                    "type_": type_map.get(prop_type, "STRING"),
                    "description": prop_def.get("description", "")
                }
            
            declarations.append(
                genai.protos.FunctionDeclaration(
                    name=tool["name"],
                    description=tool.get("description", ""),
                    parameters=genai.protos.Schema(
                        type_=genai.protos.Type.OBJECT,
                        properties={
                            k: genai.protos.Schema(
                                type_=getattr(genai.protos.Type, v["type_"]),
                                description=v["description"]
                            )
                            for k, v in properties.items()
                        },
                        required=required
                    )
                )
            )
        
        return declarations
    
    async def respond_sandbox(
        self,
        prompt: str,
        namespace: str = "travel",
        history: Optional[List[Dict]] = None
    ) -> SandboxResult:
        """
        Sandbox mode response with RAG context and remote MCP tools.
        
        1. Query RAG for relevant context
        2. Fetch tool schemas from remote MCP servers
        3. Send to Gemini with tools + RAG context
        4. Execute any tool calls via remote MCP
        5. Return final response
        """
        start = time.perf_counter()
        tools_used = []
        rag_context = []
        
        if not self._enabled:
            return SandboxResult(
                text="Gemini not configured. Set GEMINI_API_KEY.",
                latency_ms=0,
                model="mock",
                tools_used=[],
                rag_context=[]
            )
        
        # Step 1: Get RAG context
        try:
            rag_docs = await self.rag_service.search(prompt, namespace, top_k=3)
            rag_context = rag_docs
            rag_text = "\n\n".join([
                f"### {doc['title']}\n{doc['content'][:500]}..."
                for doc in rag_docs
            ]) if rag_docs else ""
        except Exception as e:
            print(f"RAG search error: {e}")
            rag_text = ""
        
        # Step 2: Get remote MCP tools based on namespace
        all_tools = []
        tool_server_map = {}  # Map tool name -> server name
        
        servers_for_namespace = [
            name for name, config in REMOTE_MCP_SERVERS.items()
            if config.get("category") == namespace
        ]
        
        for server_name in servers_for_namespace:
            tools = await self._get_remote_tools(server_name)
            for tool in tools:
                tool_server_map[tool["name"]] = server_name
            all_tools.extend(tools)
        
        # Step 3: Build Gemini model with tools
        gemini_tools = self._build_gemini_tools(all_tools)
        
        model_with_tools = genai.GenerativeModel(
            self.model_id,
            tools=gemini_tools if gemini_tools else None,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=8192
            )
        )
        
        # Step 4: Build prompt with RAG context
        system_prompt = f"""You are an intelligent assistant with access to real-time tools.

## DOMAIN KNOWLEDGE (from RAG)
{rag_text if rag_text else "No specific domain knowledge available."}

## INSTRUCTIONS
1. Use the provided domain knowledge to understand parameter formats and valid values
2. Call tools when you need real-time data (flights, hotels, places, directions)
3. Synthesize results into a helpful, structured response
4. Be specific with dates, prices, and options

## AVAILABLE TOOLS
{len(all_tools)} tools available from {len(servers_for_namespace)} servers.
"""
        
        # Convert history if provided
        chat_history = []
        if history:
            for msg in history:
                chat_history.append({
                    "role": msg.get("role", "user"),
                    "parts": [msg.get("content", "")]
                })
        
        chat = model_with_tools.start_chat(history=chat_history)
        
        # Step 5: Send message and handle tool calls
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(
            None, lambda: chat.send_message(system_prompt + "\n\nUser: " + prompt)
        )
        
        # Tool calling loop
        max_iterations = 5
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            
            if not response.candidates or not response.candidates[0].content.parts:
                break
            
            function_calls = [
                part.function_call for part in response.candidates[0].content.parts
                if hasattr(part, 'function_call') and part.function_call
            ]
            
            if not function_calls:
                break
            
            # Execute each function call via remote MCP
            function_responses = []
            for fc in function_calls:
                func_name = fc.name
                func_args = dict(fc.args) if fc.args else {}
                
                print(f"[SANDBOX TOOL] {func_name}({func_args})")
                tools_used.append(func_name)
                
                # Find which server has this tool
                server_name = tool_server_map.get(func_name)
                if server_name:
                    result = await self._call_remote_tool(server_name, func_name, func_args)
                else:
                    result = f"Tool '{func_name}' not found in any server"
                
                print(f"[SANDBOX RESULT] {func_name}: {str(result)[:200]}...")
                
                function_responses.append(
                    genai.protos.Part(
                        function_response=genai.protos.FunctionResponse(
                            name=func_name,
                            response={"result": str(result)}
                        )
                    )
                )
            
            # Send results back to model
            response = await loop.run_in_executor(
                None, lambda: chat.send_message(function_responses)
            )
        
        latency_ms = (time.perf_counter() - start) * 1000
        text = response.text if hasattr(response, "text") else str(response)
        
        return SandboxResult(
            text=text,
            latency_ms=latency_ms,
            model=self.model_id,
            tools_used=tools_used,
            rag_context=rag_context
        )
