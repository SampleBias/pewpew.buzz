# __Projects_Agent.json

Categories: Data Management, Project Management

This agent intelligently processes user requests to retrieve or update project data in a Google Sheet by determining whether to call the "Get Projects" or "Update Projects" tool. It uses GPT-4o to interpret natural language input, ensuring flexible project tracking and note updates with fallback error handling for incomplete commands.

## Technical Details

This workflow consists of 7 nodes that work together to automate your process. Here's what it uses:

- executeWorkflowTrigger: Execute Workflow Trigger
- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model
- googleSheetsTool: Get Projects, Update Projects
- set: Try Again, Success
- @n8n/n8n-nodes-langchain.agent: Projects Agent

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

