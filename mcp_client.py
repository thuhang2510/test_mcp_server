from mcp import ClientSession
from mcp.client.sse import sse_client

import asyncio
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env

async def process_query(session, query):
    anthropic = Anthropic()
    """Process a query using Claude and available tools"""
    messages = [
        {
            "role": "user",
            "content": query
        }
    ]

    response = await session.list_tools()
    available_tools = [{ 
        "name": tool.name,
        "description": tool.description,
        "input_schema": tool.inputSchema
    } for tool in response.tools]

    # print("available_tools: ", available_tools, "\n\n")

    # Initial Claude API call
    response = anthropic.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=1000,
        messages=messages,
        tools=available_tools
    )

    # print("response.content: ", response.content, "\n\n")

    # Process response and handle tool calls
    final_text = []

    for content in response.content:
        if content.type == 'text':
            final_text.append(content.text)
        elif content.type == 'tool_use':
            tool_name = content.name
            tool_args = content.input
            
            # Execute tool call
            result = await session.call_tool(tool_name, tool_args)
            final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")

            # Continue conversation with tool results
            if hasattr(content, 'text') and content.text:
                messages.append({
                    "role": "assistant",
                    "content": content.text
                })
            messages.append({
                "role": "user", 
                "content": result.content
            })

            # Get next response from Claude
            response = anthropic.messages.create(
                model="claude-opus-4-20250514",
                max_tokens=1000,
                messages=messages,
            )

            final_text.append(response.content[0].text)

    return "\n".join(final_text)

async def main():
    async with sse_client("http://127.0.0.1:8000/sse") as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()
            print("\nMCP Client Started!")
            print("Type your queries or 'quit' to exit.")
            
            while True:
                try:
                    query = input("\nQuery: ").strip()
                    
                    if query.lower() == 'quit':
                        break
                        
                    response = await process_query(session, query)
                    print("\n" + response)
                        
                except Exception as e:
                    print(f"\nError: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())