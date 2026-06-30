# mcp_client.py
"""Lớp wrapper gọi MCP server qua Streamable HTTP, dùng trong vòng lặp chat."""
import os
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


def _headers():
    key = os.getenv("MCP_API_KEY", "")
    print(f"[DEBUG] MCP_API_KEY chatbot đang gửi: '{key}'")
    return {"Authorization": f"Bearer {key}"}


def _clean_schema(schema: dict) -> dict:
    """Gemini không chấp nhận 1 số field JSON Schema mà MCP trả về
    (vd $schema, additionalProperties) -> lọc bớt trước khi đưa vào tool."""
    if not isinstance(schema, dict):
        return schema
    drop_keys = {"$schema", "additionalProperties", "title"}
    cleaned = {k: v for k, v in schema.items() if k not in drop_keys}
    if "properties" in cleaned and isinstance(cleaned["properties"], dict):
        cleaned["properties"] = {
            k: _clean_schema(v) for k, v in cleaned["properties"].items()
        }
    return cleaned


async def list_mcp_tools():
    url = os.getenv("MCP_SERVER_URL")
    try:
        async with streamablehttp_client(url, headers=_headers()) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()
                resp = await session.list_tools()
                tools = []
                for t in resp.tools:
                    tools.append({
                        "name": t.name,
                        "description": t.description or "",
                        "parameters": _clean_schema(t.inputSchema),
                    })
                return tools
    except* Exception as eg:
        for e in eg.exceptions:
            print(f"Lỗi con trong TaskGroup: {type(e).__name__}: {e}")
        raise


async def call_mcp_tool(tool_name: str, arguments: dict):
    """Gọi 1 tool cụ thể trên MCP server, trả về text kết quả."""
    url = os.getenv("MCP_SERVER_URL")
    async with streamablehttp_client(url, headers=_headers()) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, arguments=arguments)
            parts = []
            for block in result.content:
                if hasattr(block, "text"):
                    parts.append(block.text)
                else:
                    parts.append(str(block))
            return "\n".join(parts)