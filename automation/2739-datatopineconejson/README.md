# Data_to_Pinecone.json

Categories: Data Management

This workflow downloads a Google Doc, extracts the text, converts it into embeddings using OpenAI, and stores them in a Pinecone vector database. It enables semantic search and LLM-powered retrieval by preprocessing the document through text splitting and embedding before vector insertion.

## Technical Details

This workflow consists of 7 nodes that work together to automate your process. Here's what it uses:

- manualTrigger: When clicking ‘Test workflow’
- @n8n/n8n-nodes-langchain.documentDefaultDataLoader: Default Data Loader
- @n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter: Recursive Character Text Splitter
- @n8n/n8n-nodes-langchain.embeddingsOpenAi: Embeddings OpenAI
- googleDrive: Google Drive
- extractFromFile: Extract from File
- @n8n/n8n-nodes-langchain.vectorStorePinecone: Pinecone Vector Store

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

