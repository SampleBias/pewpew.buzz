# Chat with GitHub API Documentation_ RAG-Powered Chatbot with Pinecone & OpenAI

Categories: AI, Analytics, Dev Ops

Chat with GitHub API Documentation_ RAG-Powered Chatbot with Pinecone & OpenAI

## Technical Details

This workflow consists of 17 nodes that work together to automate your process. Here's what it uses:

- manualTrigger: When clicking ‘Test workflow’
- httpRequest: HTTP Request
- @n8n/n8n-nodes-langchain.vectorStorePinecone: Pinecone Vector Store, Pinecone Vector Store (Querying)
- @n8n/n8n-nodes-langchain.documentDefaultDataLoader: Default Data Loader
- @n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter: Recursive Character Text Splitter
- @n8n/n8n-nodes-langchain.chatTrigger: When chat message received
- @n8n/n8n-nodes-langchain.agent: AI Agent
- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model, OpenAI Chat Model1
- @n8n/n8n-nodes-langchain.memoryBufferWindow: Window Buffer Memory
- @n8n/n8n-nodes-langchain.toolVectorStore: Vector Store Tool
- stickyNote: Sticky Note, Sticky Note1, Sticky Note2
- @n8n/n8n-nodes-langchain.embeddingsOpenAi: Generate User Query Embedding, Generate Embeddings

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

