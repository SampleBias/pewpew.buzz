# RAG_System_2_0.json

Categories: Data Management

The RAG System 2.0 workflow in n8n is an advanced document processing and retrieval pipeline combining Google Drive automation, file conversion, data extraction, summarization, and vector embedding into Supabase. Here's what it does at a high level:

## Technical Details

This workflow consists of 47 nodes that work together to automate your process. Here's what it uses:

- aggregate: Aggregate1, Aggregate
- summarize: Summarize1, Summarize
- extractFromFile: Extract PDF Text, Extract from Excel, Extract PDF Text1, Extract from Excel1, Extract from Text File, Extract from Text File1
- set: Set File ID, Set File ID1
- supabase: Delete Old Doc Rows
- googleDrive: Download File, Delete File, Download File1, Delete File1
- httpRequest: Convert to Google Doc1, Convert to Google Doc2
- if: If
- @n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter: Recursive Character Text Splitter, Recursive Character Text Splitter1
- @n8n/n8n-nodes-langchain.embeddingsOpenAi: Embeddings OpenAI1, Embeddings OpenAI2, Embeddings OpenAI
- stickyNote: Sticky Note1, Sticky Note3, Sticky Note
- splitInBatches: Loop Over Items, Loop Over Items1
- @n8n/n8n-nodes-langchain.documentDefaultDataLoader: Enhanced Default Data Loader1, Enhanced Default Data Loader2
- googleDriveTrigger: File Created, File Updated
- @n8n/n8n-nodes-langchain.vectorStoreSupabase: Insert into Supabase Vectorstore, Supabase Vector Store, Insert into Supabase Vectorstore1
- switch: Switch, Switch2
- limit: Limit
- @n8n/n8n-nodes-langchain.chatTrigger: When chat message received
- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model, OpenAI Chat Model1
- @n8n/n8n-nodes-langchain.memoryPostgresChat: Postgres Chat Memory
- @n8n/n8n-nodes-langchain.toolVectorStore: Vector Store Tool
- @n8n/n8n-nodes-langchain.agent: New RAG Agent
- @n8n/n8n-nodes-langchain.openAi: Set Version

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

