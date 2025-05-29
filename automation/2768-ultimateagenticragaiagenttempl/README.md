# Ultimate_Agentic_RAG_AI_Agent_Template.json

Categories: AI

This template turns a Google Drive folder into a living knowledge-base: every time a file is added or updated, the workflow auto-extracts its text or tabular data, chunks it, embeds it, and stores both the vectors (for semantic search) and raw rows (for SQL) in Supabase/Postgres while keeping metadata in sync. A chat/webhook interface then powers an agent that can intelligently choose between RAG look-ups, full-document retrieval, or SQL queries on the ingested tables to answer user questions in real time.

## Technical Details

This workflow consists of 42 nodes that work together to automate your process. Here's what it uses:

- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model
- @n8n/n8n-nodes-langchain.documentDefaultDataLoader: Default Data Loader
- @n8n/n8n-nodes-langchain.embeddingsOpenAi: Embeddings OpenAI1, Embeddings OpenAI2
- stickyNote: Sticky Note, Sticky Note1, Sticky Note2, Sticky Note3, Sticky Note9
- googleDrive: Download File
- googleDriveTrigger: File Created, File Updated
- extractFromFile: Extract Document Text, Extract PDF Text, Extract from Excel, Extract from CSV
- @n8n/n8n-nodes-langchain.memoryPostgresChat: Postgres Chat Memory
- supabase: Delete Old Doc Rows, Delete Old Data Rows
- set: Set File ID, Edit Fields, Set Schema
- respondToWebhook: Respond to Webhook
- @n8n/n8n-nodes-langchain.chatTrigger: When chat message received
- webhook: Webhook
- aggregate: Aggregate
- @n8n/n8n-nodes-langchain.textSplitterCharacterTextSplitter: Character Text Splitter
- summarize: Summarize
- @n8n/n8n-nodes-langchain.agent: RAG AI Agent
- switch: Switch
- @n8n/n8n-nodes-langchain.vectorStoreSupabase: Insert into Supabase Vectorstore, Supabase Vector Store1
- postgres: Create Document Metadata Table, Create Document Rows Table (for Tabular Data), Create Documents Table and Match Function, Insert Document Metadata, Insert Table Rows, Update Schema for Document Metadata
- postgresTool: List Documents, Get File Contents, Query Document Rows
- splitInBatches: Loop Over Items

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

