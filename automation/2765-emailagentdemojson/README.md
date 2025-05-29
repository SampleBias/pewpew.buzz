# Email_Agent_Demo.json

Categories: Email

This workflow turns a plain-language request into polished Gmail actions: it can draft, send, or retrieve messages using an AI “Email Agent” that removes placeholders and always signs off as “Nate.” Behind the scenes the agent decides whether to compose or fetch emails via Gmail tools, then returns a clean response so you can see exactly what was done.

## Technical Details

This workflow consists of 6 nodes that work together to automate your process. Here's what it uses:

- executeWorkflowTrigger: Execute Workflow Trigger
- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model
- gmailTool: Send Email, Get Messages
- set: Response
- @n8n/n8n-nodes-langchain.agent: Email Agent

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

