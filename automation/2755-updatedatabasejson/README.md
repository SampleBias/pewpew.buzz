# Update_Database.json

Categories: Data Management

This workflow retrieves all files from a specific Google Drive folder, downloads and processes each one, then splits the content and embeds it using OpenAI embeddings before storing it in a Pinecone vector database under the "Restaurant" namespace. It's designed for scalable document ingestion and vector storage for semantic search or retrieval-based AI tasks.

## Technical Details

This workflow consists of 8 nodes that work together to automate your process. Here's what it uses:

- manualTrigger: When clicking ‘Test workflow’
- googleDrive: Google Drive, Get Content
- splitInBatches: Loop Over Items
- @n8n/n8n-nodes-langchain.embeddingsOpenAi: Embeddings OpenAI
- @n8n/n8n-nodes-langchain.documentDefaultDataLoader: Default Data Loader
- @n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter: Recursive Character Text Splitter
- @n8n/n8n-nodes-langchain.vectorStorePinecone: Pinecone Vector Store

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

