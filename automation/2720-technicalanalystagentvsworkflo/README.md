# Technical_Analyst_Agent_vs__Workflow.json

Categories: Analytics, Data Management

This project compares two ways to perform technical stock analysis using n8n: a workflow-based approach that processes and analyzes chart data step-by-step, and a Technical Analyst Agent that autonomously handles user requests and delegates tasks to tools like chart generators and analyzers. The agent simplifies user interaction through conversational automation, while the workflow offers greater control and modular customization.

## Technical Details

This workflow consists of 23 nodes that work together to automate your process. Here's what it uses:

- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model
- executeWorkflowTrigger: When Executed by Another Workflow
- @n8n/n8n-nodes-langchain.toolWorkflow: chart
- httpRequest: Download Chart, Get Chart, Get Chart1, Download Chart1
- @n8n/n8n-nodes-langchain.openAi: OpenAI, Get Ticker & Exchange, Analyze Chart
- telegram: Send Chart, Send Analysis, Send Chart1, Send Analysis1
- set: Response
- @n8n/n8n-nodes-langchain.agent: Technical Analyst Agent
- telegramTrigger: Telegram Trigger, Telegram Trigger1
- stickyNote: Sticky Note, Sticky Note1, Sticky Note2, Sticky Note3, Sticky Note4

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

