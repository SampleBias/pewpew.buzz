# MCP_Agent.json

Categories: Uncategorized

This MCP Agent workflow serves as a multi-tool orchestration layer, dynamically routing chat input to specific client tool APIs (like Airtable, Github, Firecrawl, Brave, and Airbnb) via LangChain’s AI routing. It intelligently interprets user prompts, selects the appropriate tool, and executes the necessary function using AI-derived parameters, enabling a scalable and unified automation interface across platforms.

## Technical Details

This workflow consists of 13 nodes that work together to automate your process. Here's what it uses:

- @n8n/n8n-nodes-langchain.lmChatOpenAi: 4o
- @n8n/n8n-nodes-langchain.chatTrigger: When chat message received
- n8n-nodes-mcp.mcpClientTool: Airbnb Actions, Airbnb Execute, Firecrawl Actions, Firecrawl Execute, Github Actions, Github Execute, Airtable Actions, Airtable Execute, Brave Actions, Brave Execute
- @n8n/n8n-nodes-langchain.agent: MCP Agent

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

