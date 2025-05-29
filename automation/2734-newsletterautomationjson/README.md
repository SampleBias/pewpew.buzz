# Newsletter_Automation.json

Categories: Content Creation

This workflow dynamically generates and sends a customized, research-backed newsletter based on a submitted topic, tone, and audience using AI content planning, internet research via Tavily, and structured writing agents. It produces hyperlinked, citation-rich HTML newsletters and delivers them via Gmail with an auto-generated, audience-specific subject line.

## Technical Details

This workflow consists of 20 nodes that work together to automate your process. Here's what it uses:

- formTrigger: On form submission
- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model
- @n8n/n8n-nodes-langchain.agent: Newsletter Expert, Research Team, Editor
- @n8n/n8n-nodes-langchain.openAi: Project Planner, Create TItle
- splitOut: Split Out
- @n8n/n8n-nodes-langchain.lmChatAnthropic: Anthropic Chat Model
- merge: Merge
- aggregate: Aggregate
- gmail: Send Newsletter
- @n8n/n8n-nodes-langchain.toolWorkflow: tavily
- executeWorkflowTrigger: Workflow Input Trigger
- httpRequest: Tavily
- set: response
- stickyNote: Sticky Note, Sticky Note1, Sticky Note2, Sticky Note3

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

