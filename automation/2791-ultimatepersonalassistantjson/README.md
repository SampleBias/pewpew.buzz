# Ultimate_Personal_Assistant.json

Categories: Content Creation

This workflow, titled "Ultimate Personal Assistant," routes voice or text messages received through Telegram to the appropriate automated agent (email, calendar, contact, blog content, or web search). It uses GPT-4o to interpret intent and dynamically call the right workflow tool, ensuring seamless execution of user requests like emailing, scheduling, or content generation.

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

