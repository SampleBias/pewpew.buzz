# API_Calls_in_n8n.json

Categories: AI

This workflow is a demo playground that lets a chat-based AI agent call three different APIs from n8n: OpenWeatherMap for live weather, Perplexity (via HTTP) for concise web summaries, and Tavily for deeper news/web searches. It showcases both the native node approach and generic HTTP-request tools, wiring them so the agent can dynamically query each service and return the results in conversation.

## Technical Details

This workflow consists of 12 nodes that work together to automate your process. Here's what it uses:

- @n8n/n8n-nodes-langchain.chatTrigger: When chat message received
- @n8n/n8n-nodes-langchain.agent: AI Agent
- @n8n/n8n-nodes-langchain.lmChatOpenRouter: GPT 4.1-mini
- openWeatherMap: OpenWeatherMap
- httpRequest: OpenWeather HTTP, Tavily
- stickyNote: Sticky Note, Sticky Note1, Sticky Note2, Sticky Note3
- httpRequestTool: Web Search
- set: Set

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

