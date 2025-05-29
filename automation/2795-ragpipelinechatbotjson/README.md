# RAG_Pipeline___Chatbot.json

Categories: Data Management

The RAG Pipeline & Chatbot workflow automatically monitors a Google Drive folder for new FAQ documents, extracts and processes their content, and stores it in Pinecone for retrieval-augmented generation. When a chat message is received, the system uses Claude 3.5 Sonnet via OpenRouter and Pinecone as a knowledge base to generate contextual, policy-aware responses in real-time.

## Technical Details

This workflow consists of 12 nodes that work together to automate your process. Here's what it uses:

- stickyNote: Sticky Note
- googleDriveTrigger: Google Drive Trigger
- googleDrive: Download File
- @n8n/n8n-nodes-langchain.vectorStorePinecone: Pinecone Vector Store, Pinecone Vector Store1
- @n8n/n8n-nodes-langchain.embeddingsOpenAi: Embeddings OpenAI, Embeddings OpenAI1
- @n8n/n8n-nodes-langchain.documentDefaultDataLoader: Default Data Loader
- @n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter: Recursive Character Text Splitter
- @n8n/n8n-nodes-langchain.agent: AI Agent
- @n8n/n8n-nodes-langchain.chatTrigger: When chat message received
- @n8n/n8n-nodes-langchain.lmChatOpenRouter: OpenRouter Chat Model

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

