"""
MCP Tools Router - Provides tool schemas for dynamic form generation
"""
import asyncio
import os
from typing import Dict, List, Any, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from ..config import get_settings

router = APIRouter(prefix="/api/mcp", tags=["mcp"])


def get_mcp_servers():
    """Get MCP server configurations with properly loaded API keys."""
    settings = get_settings()
    rapidapi_key = settings.rapidapi_key or ""
    google_maps_key = settings.google_maps_api_key or ""
    
    return {
        "rapidapi-sky": {
            "command": "npx",
            "args": ["-y", "mcp-remote", "https://mcp.rapidapi.com",
                     "--header", "x-api-host: flights-sky.p.rapidapi.com",
                     "--header", f"x-api-key: {rapidapi_key}"],
            "category": "travel"
        },
        "rapidapi-google-flights2": {
            "command": "npx",
            "args": ["-y", "mcp-remote", "https://mcp.rapidapi.com",
                     "--header", "x-api-host: google-flights2.p.rapidapi.com",
                     "--header", f"x-api-key: {rapidapi_key}"],
            "category": "travel"
        },
        "rapidapi-booking": {
            "command": "npx",
            "args": ["-y", "mcp-remote", "https://mcp.rapidapi.com",
                     "--header", "x-api-host: booking-com.p.rapidapi.com",
                     "--header", f"x-api-key: {rapidapi_key}"],
            "category": "travel"
        },
        "google-maps": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-google-maps"],
            "env": {"GOOGLE_MAPS_API_KEY": google_maps_key},
            "category": "travel"
        }
    }

class ToolSchema(BaseModel):
    name: str
    description: Optional[str] = None
    inputSchema: Optional[Dict[str, Any]] = None
    server: str
    category: str

class FormField(BaseModel):
    name: str
    type: str  # text, number, date, select, boolean
    label: str
    required: bool = False
    description: Optional[str] = None
    default: Optional[Any] = None
    options: Optional[List[str]] = None  # For select fields
    min: Optional[float] = None
    max: Optional[float] = None

class DynamicForm(BaseModel):
    toolName: str
    serverName: str
    description: Optional[str] = None
    fields: List[FormField]

def transform_schema_to_form(tool_name: str, server_name: str, description: str, input_schema: Dict) -> DynamicForm:
    """Transform MCP input schema to form fields"""
    fields = []
    properties = input_schema.get("properties", {})
    required = input_schema.get("required", [])
    
    for prop_name, prop_def in properties.items():
        field_type = "text"  # Default
        options = None
        
        # Determine field type from schema
        json_type = prop_def.get("type", "string")
        
        if json_type == "number" or json_type == "integer":
            field_type = "number"
        elif json_type == "boolean":
            field_type = "boolean"
        elif "enum" in prop_def:
            field_type = "select"
            options = prop_def["enum"]
        elif "date" in prop_name.lower():
            field_type = "date"
        
        # Create human-readable label
        label = prop_name.replace("_", " ").replace("-", " ").title()
        
        field = FormField(
            name=prop_name,
            type=field_type,
            label=label,
            required=prop_name in required,
            description=prop_def.get("description"),
            default=prop_def.get("default"),
            options=options,
            min=prop_def.get("minimum"),
            max=prop_def.get("maximum")
        )
        fields.append(field)
    
    return DynamicForm(
        toolName=tool_name,
        serverName=server_name,
        description=description,
        fields=fields
    )

async def fetch_tools_from_server(server_name: str, config: Dict) -> List[ToolSchema]:
    """Connect to MCP server and fetch tool schemas"""
    tools = []
    
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
                tools_result = await session.list_tools()
                
                for tool in tools_result.tools:
                    tools.append(ToolSchema(
                        name=tool.name,
                        description=tool.description,
                        inputSchema=tool.inputSchema,
                        server=server_name,
                        category=config.get("category", "other")
                    ))
    except Exception as e:
        print(f"Error fetching tools from {server_name}: {e}")
    
    return tools

@router.get("/servers")
async def list_servers():
    """List available MCP servers"""
    return {
        "servers": [
            {"name": name, "category": config.get("category", "other")}
            for name, config in get_mcp_servers().items()
        ]
    }

@router.get("/tools/{server_name}")
async def get_tools(server_name: str):
    """Get all tools from a specific MCP server"""
    if server_name not in get_mcp_servers():
        raise HTTPException(status_code=404, detail=f"Server '{server_name}' not found")
    
    tools = await fetch_tools_from_server(server_name, get_mcp_servers()[server_name])
    return {"server": server_name, "tools": tools, "count": len(tools)}

@router.get("/tools/{server_name}/{tool_name}/form")
async def get_tool_form(server_name: str, tool_name: str):
    """Get dynamic form schema for a specific tool"""
    if server_name not in get_mcp_servers():
        raise HTTPException(status_code=404, detail=f"Server '{server_name}' not found")
    
    tools = await fetch_tools_from_server(server_name, get_mcp_servers()[server_name])
    
    tool = next((t for t in tools if t.name == tool_name), None)
    if not tool:
        raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found in server '{server_name}'")
    
    if not tool.inputSchema:
        return DynamicForm(
            toolName=tool_name,
            serverName=server_name,
            description=tool.description,
            fields=[]
        )
    
    return transform_schema_to_form(
        tool_name=tool_name,
        server_name=server_name,
        description=tool.description,
        input_schema=tool.inputSchema
    )

@router.post("/tools/{server_name}/{tool_name}/execute")
async def execute_tool(server_name: str, tool_name: str, arguments: Dict[str, Any]):
    """Execute an MCP tool with provided arguments"""
    if server_name not in get_mcp_servers():
        raise HTTPException(status_code=404, detail=f"Server '{server_name}' not found")
    
    config = get_mcp_servers()[server_name]
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
                
                # Extract content from result
                content = []
                for item in result.content:
                    if hasattr(item, 'text'):
                        content.append({"type": "text", "text": item.text})
                    elif hasattr(item, 'data'):
                        content.append({"type": "data", "data": item.data})
                
                return {"success": True, "result": content}
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
