# PDF____Pinecone.json

Categories: Data Management

This workflow ingests a document from Google Drive, converts its contents into embeddings using OpenAI, splits the text into manageable chunks, and stores the resulting vector data into Pinecone under the customerSupport namespace. It’s designed for building a searchable knowledge base from PDFs or documents using LangChain and Pinecone integration.

## Technical Details

This workflow consists of 6 nodes that work together to automate your process. Here's what it uses:

- manualTrigger: When clicking ‘Test workflow’
- @n8n/n8n-nodes-langchain.documentDefaultDataLoader: Default Data Loader
- @n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter: Recursive Character Text Splitter
- @n8n/n8n-nodes-langchain.embeddingsOpenAi: Embeddings OpenAI
- googleDrive: Download File
- @n8n/n8n-nodes-langchain.vectorStorePinecone: Pinecone Vector Store

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

