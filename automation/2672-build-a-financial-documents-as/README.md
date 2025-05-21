# Build a Financial Documents Assistant using Qdrant and Mistral.ai

Categories: Data Management, Engineering, Finance

Build a Financial Documents Assistant using Qdrant and Mistral.ai

## Technical Details

This workflow consists of 29 nodes that work together to automate your process. Here's what it uses:

- localFileTrigger: Local File Trigger
- manualTrigger: When clicking "Test workflow"
- set: Set Variables, Prepare Embedding Document, Remap for File_Added Flow
- stickyNote: Sticky Note, Sticky Note4, Sticky Note1, Sticky Note2, Sticky Note3, Sticky Note5
- readWriteFile: Read File
- @n8n/n8n-nodes-langchain.embeddingsMistralCloud: Embeddings Mistral Cloud, Embeddings Mistral Cloud1
- @n8n/n8n-nodes-langchain.documentDefaultDataLoader: Default Data Loader
- @n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter: Recursive Character Text Splitter
- @n8n/n8n-nodes-langchain.chatTrigger: Chat Trigger
- @n8n/n8n-nodes-langchain.chainRetrievalQa: Question and Answer Chain
- @n8n/n8n-nodes-langchain.lmChatMistralCloud: Mistral Cloud Chat Model
- @n8n/n8n-nodes-langchain.retrieverVectorStore: Vector Store Retriever
- httpRequest: Search For Existing Point, Delete Existing Point, Search For Existing Point1, Delete Existing Point1
- if: Has Existing Point?, Has Existing Point?1
- switch: Handle File Event
- @n8n/n8n-nodes-langchain.vectorStoreQdrant: Qdrant Vector Store, Qdrant Vector Store1

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

