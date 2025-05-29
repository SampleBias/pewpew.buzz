# __RAG_Agent_Demo.json

Categories: AI, Data Management

his 🤖 RAG Agent Demo workflow is a Retrieval-Augmented Generation (RAG) chatbot that intelligently answers user questions by retrieving relevant project-related documents from a Supabase vector database. It uses OpenAI for language generation, stores chat context in PostgreSQL, and combines external data with conversational memory for more accurate, contextual responses.

## Technical Details

This workflow consists of 8 nodes that work together to automate your process. Here's what it uses:

- @n8n/n8n-nodes-langchain.chatTrigger: When chat message received
- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model, OpenAI Chat Model1
- @n8n/n8n-nodes-langchain.memoryPostgresChat: Postgres Chat Memory
- @n8n/n8n-nodes-langchain.vectorStoreSupabase: Supabase Vector Store
- @n8n/n8n-nodes-langchain.embeddingsOpenAi: Embeddings OpenAI
- @n8n/n8n-nodes-langchain.toolVectorStore: Vector Store Tool
- @n8n/n8n-nodes-langchain.agent: RAG Agent

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

