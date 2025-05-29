# Survey Insights with Qdrant, Python and Information Extractor

Categories: AI, Data Management

Survey Insights with Qdrant, Python and Information Extractor

## Technical Details

This workflow consists of 42 nodes that work together to automate your process. Here's what it uses:

- @n8n/n8n-nodes-langchain.embeddingsOpenAi: Embeddings OpenAI
- @n8n/n8n-nodes-langchain.documentDefaultDataLoader: Default Data Loader
- set: Convert to Question Answer Pairs, Extract Questions, Set Variables, Prep Output For Export, Prep Values For Trigger, Prep Values For Export
- @n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter: Recursive Character Text Splitter
- googleSheets: Get Survey Results, Get Survey Headers, Export To Sheets, Export To Sheets1, Create Insights Sheet
- splitOut: Questions to List, Clusters To List, QA Pairs to List
- httpRequest: Find All Answers, Get Payload of Points, Get Sheet Details
- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model
- splitInBatches: For Each Question...
- executeWorkflow: Trigger Insights
- executeWorkflowTrigger: Execute Workflow Trigger
- stickyNote: Sticky Note, Sticky Note1, Sticky Note2, Sticky Note3, Sticky Note4, Sticky Note5, Sticky Note6, Sticky Note7, Sticky Note8, Sticky Note9, Sticky Note10, Sticky Note11
- if: Has Clusters?
- manualTrigger: When clicking ‘Test workflow’
- filter: Only Clusters With 3+ points
- code: Apply K-means Clustering Algorithm
- @n8n/n8n-nodes-langchain.vectorStoreQdrant: Qdrant Vector Store
- @n8n/n8n-nodes-langchain.informationExtractor: Survey Insights Agent

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

