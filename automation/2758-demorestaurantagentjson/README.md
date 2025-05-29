# Demo_Restaurant_Agent.json

Categories: Data Management

This workflow turns GPT-4o into a friendly “restaurant assistant” that answers staff questions about menu items, policies, feedback, and hours. Each time it’s asked something, it queries a Pinecone vector store of restaurant knowledge to return accurate, upbeat replies with a dash of humor and emojis.

## Technical Details

This workflow consists of 8 nodes that work together to automate your process. Here's what it uses:

- @n8n/n8n-nodes-langchain.manualChatTrigger: When chat message received
- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model, OpenAI Chat Model1
- @n8n/n8n-nodes-langchain.memoryBufferWindow: Window Buffer Memory
- @n8n/n8n-nodes-langchain.toolVectorStore: Vector Store Tool
- @n8n/n8n-nodes-langchain.embeddingsOpenAi: Embeddings OpenAI
- @n8n/n8n-nodes-langchain.agent: AI Agent
- @n8n/n8n-nodes-langchain.vectorStorePinecone: Pinecone Vector Store

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

