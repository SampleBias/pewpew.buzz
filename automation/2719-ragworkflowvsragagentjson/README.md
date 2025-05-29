# RAG_Workflow_vs__RAG_Agent.json

Categories: AI

This workflow contrasts a manual RAG pipeline, where each step (embedding, retrieval, response) is built node-by-node, with an autonomous RAG agent that uses tools and an LLM to handle the process conversationally. The agent is faster to build, while the workflow offers more control and customization.

## Technical Details

This workflow consists of 23 nodes that work together to automate your process. Here's what it uses:

- manualTrigger: When clicking ‘Test workflow’
- googleDrive: Download File
- @n8n/n8n-nodes-langchain.vectorStorePinecone: Pinecone Vector Store, Pinecone, Search Knowledge Base
- @n8n/n8n-nodes-langchain.embeddingsOpenAi: Embeddings OpenAI, Embeddings OpenAI1, Embeddings OpenAI2
- @n8n/n8n-nodes-langchain.documentDefaultDataLoader: Default Data Loader
- @n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter: Recursive Character Text Splitter
- stickyNote: Sticky Note, Sticky Note1, Sticky Note2, Sticky Note3
- @n8n/n8n-nodes-langchain.lmChatGoogleGemini: 2.0 Flash
- gmailTrigger: Gmail Trigger, Gmail Trigger1
- @n8n/n8n-nodes-langchain.agent: Customer Support Agent
- @n8n/n8n-nodes-langchain.openAi: Write Email
- filter: Filter
- aggregate: Aggregate
- gmail: Reply to Customer
- gmailTool: Reply Email

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

