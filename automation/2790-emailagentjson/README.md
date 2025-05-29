# __Email_Agent.json

Categories: Email

This n8n workflow sets up an AI-powered email assistant using GPT-4o to manage Gmail tasks like sending, replying, labeling, drafting, and retrieving emails. The agent processes natural language requests and translates them into Gmail API actions, ensuring professional HTML email formatting and error handling.

## Technical Details

This workflow consists of 12 nodes that work together to automate your process. Here's what it uses:

- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model
- set: Try Again, Success
- @n8n/n8n-nodes-langchain.agent: Email Agent
- gmailTool: Send Email, Get Emails, Create Draft, Email Reply, Get Labels, Label Emails, Mark Unread
- executeWorkflowTrigger: When Executed by Another Workflow

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

