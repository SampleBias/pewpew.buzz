# AI_Personal_Assistant.json

Categories: Email, Project Management

This workflow turns Telegram messages (text or voice) into actions using an AI-powered personal assistant. It can transcribe voice notes, manage contacts, access calendars and emails, perform research, and reply with summarized text or voice—all through a conversational interface.

## Technical Details

This workflow consists of 20 nodes that work together to automate your process. Here's what it uses:

- telegramTrigger: Telegram Trigger
- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model, OpenAI Chat Model1
- @n8n/n8n-nodes-langchain.memoryBufferWindow: Window Buffer Memory
- googleSheetsTool: Contact Database
- telegram: Response, Download Voice File, Send Audio
- @n8n/n8n-nodes-langchain.toolWorkflow: researchAgent, calendarAgent, emailAgent
- set: Set 'Text'
- @n8n/n8n-nodes-langchain.openAi: Transcribe Audio, Summarize Agent Response
- switch: Switch
- httpRequest: Create Audio
- @n8n/n8n-nodes-langchain.toolVectorStore: Vector Store Tool
- @n8n/n8n-nodes-langchain.vectorStorePinecone: Pinecone Vector Store
- @n8n/n8n-nodes-langchain.embeddingsOpenAi: Embeddings OpenAI
- @n8n/n8n-nodes-langchain.agent: Personal Assistant

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

