# Building RAG Chatbot for Movie Recommendations with Qdrant and Open AI

Categories: AI, Content Creation, Customer Support

Building RAG Chatbot for Movie Recommendations with Qdrant and Open AI

## Technical Details

This workflow consists of 27 nodes that work together to automate your process. Here's what it uses:

- manualTrigger: When clicking ‘Test workflow’
- github: GitHub
- extractFromFile: Extract from File
- @n8n/n8n-nodes-langchain.embeddingsOpenAi: Embeddings OpenAI
- @n8n/n8n-nodes-langchain.documentDefaultDataLoader: Default Data Loader
- @n8n/n8n-nodes-langchain.textSplitterTokenSplitter: Token Splitter
- @n8n/n8n-nodes-langchain.vectorStoreQdrant: Qdrant Vector Store
- @n8n/n8n-nodes-langchain.chatTrigger: When chat message received
- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model
- @n8n/n8n-nodes-langchain.toolWorkflow: Call n8n Workflow Tool
- @n8n/n8n-nodes-langchain.memoryBufferWindow: Window Buffer Memory
- executeWorkflowTrigger: Execute Workflow Trigger
- merge: Merge, Merge1
- splitOut: Split Out, Split Out1
- aggregate: Aggregate
- @n8n/n8n-nodes-langchain.agent: AI Agent
- httpRequest: Embedding Recommendation Request with Open AI, Embedding Anti-Recommendation Request with Open AI, Calling Qdrant Recommendation API, Retrieving Recommended Movies Meta Data
- set: Extracting Embedding, Extracting Embedding1, Selecting Fields Relevant for Agent
- stickyNote: Sticky Note, Sticky Note1

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

