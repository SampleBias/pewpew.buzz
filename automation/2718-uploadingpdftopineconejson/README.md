# Uploading_PDF_to_Pinecone.json

Categories: Data Management

This bot automates the process of downloading a PDF from Google Drive, extracting and splitting its content, generating OpenAI embeddings, and storing them in a Pinecone vector database for fast, intelligent search. It enables future bots or agents to answer natural language questions about the PDF’s contents using vector search.

## Technical Details

This workflow consists of 6 nodes that work together to automate your process. Here's what it uses:

- manualTrigger: When clicking ‘Test workflow’
- googleDrive: Google Drive
- @n8n/n8n-nodes-langchain.embeddingsOpenAi: Embeddings OpenAI
- @n8n/n8n-nodes-langchain.documentDefaultDataLoader: Default Data Loader
- @n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter: Recursive Character Text Splitter
- @n8n/n8n-nodes-langchain.vectorStorePinecone: Pinecone Vector Store

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

