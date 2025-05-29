# Nike_Agent.json

Categories: Analytics

The Nike Agent bot is a conversational assistant that answers user questions about Nike’s earnings using a vector database of financial data. It responds in a fun, engaging tone with emojis, jokes, and real-time facts pulled from sources like Pinecone, OpenAI, and Wikipedia.

## Technical Details

This workflow consists of 10 nodes that work together to automate your process. Here's what it uses:

- @n8n/n8n-nodes-langchain.manualChatTrigger: When chat message received
- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model, OpenAI Chat Model1
- @n8n/n8n-nodes-langchain.memoryBufferWindow: Window Buffer Memory
- @n8n/n8n-nodes-langchain.toolVectorStore: Vector Store Tool
- @n8n/n8n-nodes-langchain.vectorStorePinecone: Pinecone Vector Store
- @n8n/n8n-nodes-langchain.embeddingsOpenAi: Embeddings OpenAI
- @n8n/n8n-nodes-langchain.agent: Nike Agent
- @n8n/n8n-nodes-langchain.toolWikipedia: Wikipedia
- @n8n/n8n-nodes-langchain.toolCalculator: Calculator

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

