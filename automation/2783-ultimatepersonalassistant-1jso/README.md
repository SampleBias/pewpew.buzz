# Ultimate_Personal_Assistant (1).json

Categories: AI, Data Management, Email

This n8n workflow sets up an AI-powered personal assistant via Telegram that intelligently routes user queries to the appropriate tool—such as email, calendar, contact management, content creation, or web search—based on context. It includes voice transcription, memory handling, and dynamic tool execution through OpenAI, making it a fully automated command center for everyday productivity.

## Technical Details

This workflow consists of 15 nodes that work together to automate your process. Here's what it uses:

- @n8n/n8n-nodes-langchain.agent: Ultimate Assistant
- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model
- @n8n/n8n-nodes-langchain.toolWorkflow: Email Agent, Contact Agent, Content Creator Agent, Calendar Agent
- @n8n/n8n-nodes-langchain.memoryBufferWindow: Window Buffer Memory
- @n8n/n8n-nodes-langchain.toolHttpRequest: Tavily
- @n8n/n8n-nodes-langchain.toolCalculator: Calculator
- telegramTrigger: Telegram Trigger
- set: Set 'Text'
- switch: Switch
- telegram: Response, Download File
- @n8n/n8n-nodes-langchain.openAi: Transcribe

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

