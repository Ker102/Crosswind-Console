"""
Sandbox LLM Service - LangChain-based agent with RAG + Remote MCP tools
Uses persistent HTTP MCP client for fast tool calls.
LangChain 1.x API with bind_tools() pattern.
"""
import os
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from .mcp_client import get_mcp_client, PersistentMCPClient
from .rag_service import RAGService


@dataclass
class SandboxResult:
    text: str
    latency_ms: float
    model: str
    tools_used: List[str]
    rag_context: List[Dict]


class LangChainSandboxService:
    """
    LangChain-based Sandbox service with:
    - Gemini LLM via langchain-google-genai
    - Supabase RAG retriever
    - Persistent MCP client for remote tools (via bind_tools)
    """
    
    def __init__(self, gemini_api_key: str, model_id: str = "gemini-2.0-flash"):
        self.model_id = model_id
        self._api_key = gemini_api_key
        self._enabled = bool(gemini_api_key)
        
        # Initialize LangChain Gemini LLM
        if self._enabled:
            self.base_llm = ChatGoogleGenerativeAI(
                model=model_id,
                google_api_key=gemini_api_key,
                max_output_tokens=8192,
                temperature=0.7
            )
        else:
            self.base_llm = None
        
        # RAG service for context retrieval
        self.rag_service = RAGService()
        
        # MCP client for remote tools
        self.mcp_client = get_mcp_client()
        
        # LangChain tools
        self._tools = self._create_tools()
        
        # LLM with tools bound
        if self._enabled and self._tools:
            self.llm = self.base_llm.bind_tools(self._tools)
        else:
            self.llm = self.base_llm
    
    def _create_tools(self) -> List:
        """Create LangChain tool functions for MCP integration"""
        
        mcp_client = self.mcp_client
        
        @tool
        async def search_flights_sky(
            origin: str,
            destination: str,
            date: str,
            adults: int = 1,
            cabin_class: str = "economy"
        ) -> str:
            """Search for flights using Skyscanner/Flights Sky API. 
            
            Args:
                origin: Origin IATA airport code (e.g., LHR, JFK)
                destination: Destination IATA airport code
                date: Departure date in YYYY-MM-DD format
                adults: Number of adult passengers
                cabin_class: Cabin class (economy, business, first)
            """
            result = await mcp_client.call_tool(
                service="flights-sky",
                tool_name="searchFlights",
                arguments={
                    "originSkyId": origin.upper(),
                    "destinationSkyId": destination.upper(),
                    "date": date,
                    "adults": adults,
                    "cabinClass": cabin_class.upper()
                }
            )
            return result.content if result.success else f"Error: {result.error}"
        
        @tool
        async def search_google_flights(
            departure_id: str,
            arrival_id: str,
            outbound_date: str,
            adults: int = 1
        ) -> str:
            """Search for flights using Google Flights2 API.
            
            Args:
                departure_id: Origin IATA code (e.g., LHR, JFK)
                arrival_id: Destination IATA code
                outbound_date: Departure date in YYYY-MM-DD format
                adults: Number of adult passengers
            """
            result = await mcp_client.call_tool(
                service="google-flights2",
                tool_name="search_flights",
                arguments={
                    "departure_id": departure_id.upper(),
                    "arrival_id": arrival_id.upper(),
                    "outbound_date": outbound_date,
                    "adults": adults,
                    "travel_class": "1"
                }
            )
            return result.content if result.success else f"Error: {result.error}"
        
        @tool
        async def search_booking_hotels(
            destination: str,
            checkin_date: str,
            checkout_date: str,
            adults: int = 1
        ) -> str:
            """Search for hotels using Booking.com API.
            
            Args:
                destination: City name or destination ID
                checkin_date: Check-in date in YYYY-MM-DD format
                checkout_date: Check-out date in YYYY-MM-DD format
                adults: Number of adult guests
            """
            result = await mcp_client.call_tool(
                service="booking",
                tool_name="Search_hotels",
                arguments={
                    "dest_id": destination,
                    "checkin_date": checkin_date,
                    "checkout_date": checkout_date,
                    "adults_number": adults
                }
            )
            return result.content if result.success else f"Error: {result.error}"
        
        return [search_flights_sky, search_google_flights, search_booking_hotels]
    
    def _build_system_message(self, namespace: str, rag_context: List[Dict]) -> str:
        """Build system message with RAG context"""
        
        # Format RAG context
        context_text = ""
        if rag_context:
            context_parts = []
            for doc in rag_context[:3]:
                context_parts.append(f"[{doc.get('title', 'Document')}]\n{doc.get('content', '')[:500]}")
            context_text = "\n\n".join(context_parts)
        
        return f"""You are a helpful travel assistant with access to real-time flight and hotel search tools.

## API Parameter Guidance (from RAG):
{context_text}

## Instructions:
1. Use the tools to search for flights, hotels, or other travel information
2. Always use IATA airport codes (e.g., LHR for London Heathrow, JFK for New York JFK)
3. Use date format YYYY-MM-DD
4. Present results in a clear, formatted way
5. Compare prices from multiple sources when possible

Current namespace: {namespace}
"""
    
    async def process(
        self,
        prompt: str,
        namespace: str = "travel",
        history: Optional[List[Dict]] = None
    ) -> SandboxResult:
        """
        Process a user prompt using LangChain with bind_tools pattern.
        
        Args:
            prompt: User's question or request
            namespace: RAG namespace for context retrieval
            history: Previous conversation messages
        
        Returns:
            SandboxResult with response text, latency, and metadata
        """
        if not self._enabled:
            return SandboxResult(
                text="LLM service not configured",
                latency_ms=0,
                model=self.model_id,
                tools_used=[],
                rag_context=[]
            )
        
        start_time = time.time()
        tools_used = []
        
        # Retrieve RAG context
        rag_context = []
        try:
            rag_results = await self.rag_service.search(prompt, namespace=namespace, limit=3)
            rag_context = rag_results if rag_results else []
        except Exception as e:
            print(f"RAG search error: {e}")
        
        # Build messages
        messages = [
            SystemMessage(content=self._build_system_message(namespace, rag_context))
        ]
        
        # Add history
        if history:
            for msg in history:
                if msg.get("role") == "user":
                    messages.append(HumanMessage(content=msg.get("content", "")))
                elif msg.get("role") == "assistant":
                    messages.append(AIMessage(content=msg.get("content", "")))
        
        # Add current prompt
        messages.append(HumanMessage(content=prompt))
        
        try:
            # Invoke LLM with tools
            response = await self.llm.ainvoke(messages)
            
            # Loop for multi-turn tool execution (max 5 iterations)
            MAX_ITERATIONS = 5
            for _ in range(MAX_ITERATIONS):
                if not (hasattr(response, 'tool_calls') and response.tool_calls):
                    break
                    
                tool_results = []
                # Execute all tool calls from this turn
                for tool_call in response.tool_calls:
                    tool_name = tool_call.get("name", "")
                    tool_args = tool_call.get("args", {})
                    tools_used.append(tool_name)
                    
                    # Find and execute the tool
                    tool_found = False
                    for t in self._tools:
                        if t.name == tool_name:
                            try:
                                result = await t.ainvoke(tool_args)
                                tool_results.append(f"[{tool_name}]: {result}")
                            except Exception as e:
                                tool_results.append(f"[{tool_name}]: Error - {e}")
                            tool_found = True
                            break
                    if not tool_found:
                        tool_results.append(f"[{tool_name}]: Error - Tool not found")
                
                # Append tool results to messages
                if tool_results:
                    messages.append(response)
                    # Use standard string concatenation, not f-string
                    messages.append(HumanMessage(content="Tool Results:\n" + "\n".join(tool_results)))
                    
                    # Get next response from LLM
                    response = await self.base_llm.ainvoke(messages)
                    response_text = response.content
                else:
                    response_text = response.content
                    break
            
            # Final response text (if loop finished or no tools called)
            if not response_text:
                response_text = response.content
            
        except Exception as e:
            response_text = f"Error processing request: {str(e)}"
            print(f"LLM error: {e}")
            import traceback
            traceback.print_exc()
        
        latency_ms = (time.time() - start_time) * 1000
        
        return SandboxResult(
            text=response_text,
            latency_ms=latency_ms,
            model=self.model_id,
            tools_used=tools_used,
            rag_context=rag_context
        )


# Factory function for dependency injection
def create_sandbox_service(gemini_api_key: str, model_id: str = "gemini-2.0-flash") -> LangChainSandboxService:
    """Create a new LangChain sandbox service instance"""
    return LangChainSandboxService(gemini_api_key, model_id)
