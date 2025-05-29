# Tool__Doc_to_Pinecone.json

Categories: Data Management

This "Tool: Doc to Pinecone" workflow downloads a Google Doc, splits the content using a recursive character splitter, generates embeddings with OpenAI, and stores them in the "resorts" namespace of a Pinecone vector database. It's designed for converting document-based resort data into a searchable vector format.

## Technical Details

This workflow consists of 6 nodes that work together to automate your process. Here's what it uses:

- manualTrigger: When clicking ‘Test workflow’
- googleDrive: Download File
- @n8n/n8n-nodes-langchain.vectorStorePinecone: Pinecone Vector Store
- @n8n/n8n-nodes-langchain.documentDefaultDataLoader: Default Data Loader
- @n8n/n8n-nodes-langchain.embeddingsOpenAi: Embeddings OpenAI
- @n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter: Recursive Character Text Splitter

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

