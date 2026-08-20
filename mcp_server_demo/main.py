# FastMCP is a framework for building MCP Servers with tools, prompts and resources
from fastmcp import FastMCP


# the name of the server
mcp = FastMCP("Math and Weather Server")


# Let's have the first tool for adding
@mcp.tool
def add_numbers(a: float, b: float) -> float:
   """Adds two numbers together."""
   return a + b


# now the second tool for subtracting
@mcp.tool
def subtract_numbers(a: float, b: float) -> float:
   """Subtracts the second number from the first."""
   return a - b


if __name__ == "__main__":
   # Run with HTTP transport -- remote connection is possible
   mcp.run(transport="http", host="127.0.0.1", port=9001)
   # run over stdio
   # mcp.run(transport="stdio")
