# Supabase_Postgres.json

Categories: Data Management

This workflow sets up a chat-based RAG assistant that remembers conversations in Postgres and answers new queries by searching a Supabase-backed vector store of company documents. A manual trigger lets you ingest Google Drive files, chunk and

## Technical Details

This workflow consists of 15 nodes that work together to automate your process. Here's what it uses:

- @n8n/n8n-nodes-langchain.chatTrigger: When chat message received
- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model
- @n8n/n8n-nodes-langchain.memoryPostgresChat: Postgres Chat Memory
- @n8n/n8n-nodes-langchain.vectorStoreSupabase: Supabase Vector Store, Add to Supabase
- @n8n/n8n-nodes-langchain.embeddingsOpenAi: Embeddings OpenAI, Embeddings
- @n8n/n8n-nodes-langchain.documentDefaultDataLoader: Default Data Loader
- @n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter: Recursive Character Text Splitter
- manualTrigger: When clicking ‘Test workflow’
- googleDrive: Download File
- @n8n/n8n-nodes-langchain.agent: RAG Agent
- stickyNote: Sticky Note, Sticky Note1, Sticky Note2

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

