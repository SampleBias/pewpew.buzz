# o3_mini_Travel_Agent.json

Categories: Uncategorized

Gathers info about resorts, flights, and creates iteneraries

## Technical Details

This workflow consists of 9 nodes that work together to automate your process. Here's what it uses:

- @n8n/n8n-nodes-langchain.chatTrigger: When chat message received
- @n8n/n8n-nodes-langchain.vectorStorePinecone: Activities, Flights, Resorts
- @n8n/n8n-nodes-langchain.embeddingsOpenAi: Embeddings OpenAI
- @n8n/n8n-nodes-langchain.memoryBufferWindow: Window Buffer Memory
- @n8n/n8n-nodes-langchain.agent: o3 mini Travel Agent
- gmailTool: Send Itinerary
- @n8n/n8n-nodes-langchain.lmChatOpenRouter: OpenRouter Chat Model

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

