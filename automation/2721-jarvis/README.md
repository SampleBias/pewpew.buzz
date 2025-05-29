# Jarvis

Categories: Data Management, Email, Content Creation

This JARVIS agent acts as a universal personal assistant that routes user requests to the correct specialized workflow tools—like email, calendar, contacts, blog content creation, or web search. It uses OpenAI for intent detection and decision-making, ensuring actions are delegated without handling any content creation directly.

## Technical Details

This workflow consists of 15 nodes that work together to automate your process. Here's what it uses:

- @n8n/n8n-nodes-langchain.toolWorkflow: Email Agent, Contact Agent, Content Creator Agent, Calendar Agent
- @n8n/n8n-nodes-langchain.toolHttpRequest: Tavily
- @n8n/n8n-nodes-langchain.toolCalculator: Calculator
- webhook: Webhook
- respondToWebhook: Respond to Webhook
- @n8n/n8n-nodes-langchain.agent: Jarvis
- @n8n/n8n-nodes-langchain.lmChatOpenAi: 4o
- @n8n/n8n-nodes-langchain.memoryBufferWindow: Simple Memory
- stickyNote: Sticky Note, Sticky Note1, Sticky Note2, Sticky Note3

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

