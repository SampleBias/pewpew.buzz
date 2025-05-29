# Customer Insights with Qdrant, Python and Information Extractor

Categories: AI, Analytics, Project Management

Customer Insights with Qdrant, Python and Information Extractor

## Technical Details

This workflow consists of 37 nodes that work together to automate your process. Here's what it uses:

- manualTrigger: When clicking ‘Test workflow’
- set: Zip Entries, Set Variables, Set Variables1, Prep Output For Export, Prep Values For Trigger
- html: Extract Reviews
- splitOut: Reviews to List, Clusters To List
- @n8n/n8n-nodes-langchain.documentDefaultDataLoader: Default Data Loader
- @n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter: Recursive Character Text Splitter
- @n8n/n8n-nodes-langchain.embeddingsOpenAi: Embeddings OpenAI
- httpRequest: Get Payload of Points, Find Reviews, Clear Existing Reviews, Get TrustPilot Page
- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model
- filter: Only Clusters With 3+ points
- googleSheets: Export To Sheets
- executeWorkflow: Trigger Insights
- executeWorkflowTrigger: Execute Workflow Trigger
- stickyNote: Sticky Note, Sticky Note1, Sticky Note2, Sticky Note3, Sticky Note4, Sticky Note5, Sticky Note7, Sticky Note8, Sticky Note6, Sticky Note9, Sticky Note10, Sticky Note12, Sticky Note11
- @n8n/n8n-nodes-langchain.vectorStoreQdrant: Qdrant Vector Store
- code: Apply K-means Clustering Algorithm
- @n8n/n8n-nodes-langchain.informationExtractor: Customer Insights Agent

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

