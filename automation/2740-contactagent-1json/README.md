# __Contact_Agent (1).json

Categories: Data Management

This workflow uses a language model to interpret natural language queries for contact management, enabling users to look up, add, or update contacts in Airtable. It routes requests through the agent, which determines whether to search or upsert records, and gracefully handles both successful updates and error cases.

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

