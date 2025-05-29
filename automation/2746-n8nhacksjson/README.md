# n8n_Hacks.json

Categories: AI

This workflow is a comprehensive sandbox of advanced n8n automations showcasing AI agents, API integrations, and error handling techniques. It serves as a modular reference for building intelligent, multi-channel automation workflows.

## Technical Details

This workflow consists of 75 nodes that work together to automate your process. Here's what it uses:

- set: 1, Answer, Expression, Array, Edit Fields, Set, Example, Workflow Variables, Set Text, Edit Fields1
- wait: 2
- @n8n/n8n-nodes-langchain.openAi: 3
- manualTrigger: When clicking ‘Test workflow’
- httpRequest: Perplexity, Perplexity1, Tavily, OpenAI, Web Search, HTTP Request, HTTP Request1
- stickyNote: Sticky Note, Sticky Note1, Sticky Note2, Sticky Note3, Sticky Note4, Sticky Note5, Sticky Note6, Sticky Note7, Sticky Note8, Sticky Note11, Sticky Note12, Sticky Note9, Sticky Note10, Sticky Note13, Sticky Note14, Sticky Note15, Sticky Note16, Sticky Note17, Sticky Note18, Sticky Note19, Sticky Note20, Sticky Note21, Sticky Note22, Sticky Note23, Sticky Note24, Sticky Note25, Sticky Note26
- @n8n/n8n-nodes-langchain.lmChatOpenRouter: OpenRouter Chat Model, OpenRouter Chat Model1, OpenRouter Chat Model2, OpenRouter Chat Model3, OpenRouter Chat Model4
- @n8n/n8n-nodes-langchain.agent: Current Time, AI Agent, AI Agent1, AI Agent2, AI Agent3
- splitInBatches: Loop Over Items
- code: Set URLs
- gmail: Gmail, Gmail1
- telegram: Telegram
- slack: Slack, Slack1
- errorTrigger: Error Trigger
- executeWorkflowTrigger: When Executed by Another Workflow
- aggregate: Aggregate
- @n8n/n8n-nodes-langchain.toolWorkflow: Email Agent
- merge: Merge
- @n8n/n8n-nodes-langchain.chatTrigger: When chat message received
- telegramTrigger: Telegram Trigger
- discord: Discord
- googleChat: Google Chat
- splitOut: Split Out
- @n8n/n8n-nodes-langchain.outputParserStructured: Structured Output Parser

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

