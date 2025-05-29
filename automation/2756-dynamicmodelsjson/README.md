# Dynamic_Models.json

Categories: AI

This workflow dynamically selects the best AI model for each user query based on task type. It routes responses, performs tool actions, and logs everything through Slack and Google Sheets.

## Technical Details

This workflow consists of 43 nodes that work together to automate your process. Here's what it uses:

- @n8n/n8n-nodes-langchain.lmChatOpenRouter: Gemini 2.0 Flash, Dynamic Brain, Gemini 2.0-Flash, Dynamic-Brain
- @n8n/n8n-nodes-langchain.agent: Model Selector, Smarty Pants, RAG Agent, Model-Selector
- gmailTool: Create Draft
- airtableTool: Contacts
- googleCalendarTool: Create Event
- @n8n/n8n-nodes-langchain.toolHttpRequest: Tavily
- googleSheets: Log Output
- slackTrigger: Slack Trigger
- slack: Slack
- stickyNote: Sticky Note, Sticky Note1, Sticky Note2, Sticky Note3, Sticky Note4, Sticky Note5, Sticky Note6, Sticky Note7, Sticky Note13, Sticky Note14, Sticky Note15, Sticky Note16, Sticky Note8, Sticky Note9, Sticky Note10, Sticky Note11, Sticky Note12, Sticky Note17, Sticky Note18
- manualTrigger: When clicking ‘Test workflow’
- googleDrive: Download File
- @n8n/n8n-nodes-langchain.vectorStoreSupabase: Supabase Vector Store, knowledgeBase
- @n8n/n8n-nodes-langchain.documentDefaultDataLoader: Default Data Loader
- @n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter: Recursive Character Text Splitter
- @n8n/n8n-nodes-langchain.embeddingsOpenAi: Embeddings_OpenAI, Embeddings OpenAI
- @n8n/n8n-nodes-langchain.chatTrigger: When chat message received

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

