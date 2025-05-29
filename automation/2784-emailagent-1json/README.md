# __Email_Agent (1).json

Categories: Email

This Email Agent workflow uses a GPT-4o-powered LangChain agent to interpret user email-related requests and dynamically route them to the correct Gmail action—such as sending, drafting, replying, labeling, or marking emails as unread. It includes built-in fallback handling and responds with success or retry messages based on execution results.

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

