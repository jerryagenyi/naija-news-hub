#!/bin/bash

echo "Testing Context7 MCP server..."
npx -y @upstash/context7-mcp@latest --help

echo -e "\n\nTesting Brave Search MCP server..."
npx -y @modelcontextprotocol/server-brave-search --help
