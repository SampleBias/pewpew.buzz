# __Contact_Agent (2).json

Categories: Data Management

This workflow enables an AI agent to manage contacts in Airtable by searching for existing entries or adding/updating contact information based on user queries. It uses OpenAI for understanding the input and Airtable integration for seamless contact database operations.

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

