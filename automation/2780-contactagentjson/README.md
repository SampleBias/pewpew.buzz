# __Contact_Agent.json

Categories: AI

This workflow exposes a “Contact Agent” that, when triggered (either manually or by another workflow), parses the user’s query, looks up or upserts contact details in an Airtable “Contacts” base via AI-driven instructions, and returns a response string. It leverages GPT-4o to decide when to call the “Get Contacts” or “Add or Update Contact” tools, then outputs either the AI-generated result or a fallback error message.

## Technical Details

This workflow consists of 7 nodes that work together to automate your process. Here's what it uses:

- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model
- airtableTool: Get Contacts, Add or Update Contact
- @n8n/n8n-nodes-langchain.agent: Contact Agent
- set: Response, Try Again
- executeWorkflowTrigger: When Executed by Another Workflow

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

