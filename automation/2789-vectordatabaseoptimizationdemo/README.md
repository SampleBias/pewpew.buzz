# Vector_Database_Optimization_Demo.json

Categories: Data Management

This workflow tests multiple methods for processing and embedding documents into Pinecone, comparing text splitting strategies, metadata inclusion, and embedding models. It helps optimize vector search accuracy and performance across varied document ingestion pipelines.

## Technical Details

This workflow consists of 65 nodes that work together to automate your process. Here's what it uses:

- manualTrigger: When clicking ‘Test workflow’
- @n8n/n8n-nodes-langchain.embeddingsOpenAi: Embeddings OpenAI, Embeddings OpenAI1, Embeddings OpenAI2, Embeddings OpenAI3, Embeddings OpenAI4, Embeddings OpenAI5, Embeddings OpenAI6, Embeddings OpenAI7, Embeddings OpenAI8
- @n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter: Recursive Character Text Splitter, Recursive Character Text Splitter1, Recursive Character Text Splitter2, Recursive Character Text Splitter3, Recursive Character Text Splitter4, Recursive Character Text Splitter5
- googleDrive: Google Drive, Google Drive1, Google Drive2, Google Drive3, Google Drive4, Google Drive5, Google Drive6, Google Drive7, Google Drive8
- extractFromFile: Extract from File, Extract from File1, Extract from File2, Extract from File3, Extract from File4, Extract from File5, Extract from File6
- stickyNote: Sticky Note, Sticky Note1, Sticky Note2, Sticky Note3, Sticky Note4, Sticky Note5, Sticky Note6, Sticky Note7, Sticky Note8
- @n8n/n8n-nodes-langchain.documentDefaultDataLoader: Default Data Loader1, Default Data Loader2, Default Data Loader3, Default Data Loader4, Default Data Loader5, JSON, Binary, Binary1
- @n8n/n8n-nodes-langchain.vectorStorePinecone: Pinecone Vector Store2, Pinecone Vector Store3, Pinecone Vector Store5, Pinecone Vector Store4, Pinecone Vector Store, Pinecone Vector Store7, Pinecone Vector Store8, Pinecone Vector Store1, Pinecone Vector Store6
- set: Get Content, Get Content1, Get Content2, Get Content3, Get Content4
- @n8n/n8n-nodes-langchain.textSplitterTokenSplitter: Token Splitter
- @n8n/n8n-nodes-langchain.textSplitterCharacterTextSplitter: Character Text Splitter

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

