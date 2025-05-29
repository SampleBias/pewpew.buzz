# Voice_RAG_Agent.json

Categories: AI

This webhook-based RAG flow takes an incoming question (e.g., from a voice transcript), fetches related “projects” knowledge from a Pinecone vector store, and runs GPT-4o to craft an answer. It then immediately returns the AI’s response to the caller via the same webhook.

## Technical Details

This workflow consists of 8 nodes that work together to automate your process. Here's what it uses:

- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model, OpenAI Chat Model1
- @n8n/n8n-nodes-langchain.embeddingsOpenAi: Embeddings OpenAI
- respondToWebhook: Respond to Webhook
- @n8n/n8n-nodes-langchain.toolVectorStore: projects
- @n8n/n8n-nodes-langchain.agent: AI Agent
- webhook: Webhook
- @n8n/n8n-nodes-langchain.vectorStorePinecone: Pinecone Vector Store

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

