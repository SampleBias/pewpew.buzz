# Parent_Agent.json

Categories: Content Creation

The Parent Agent takes user story prompts and extracts the setting, main character, and adventure. It forwards these details to the Story Agent workflow, which generates the actual story.

## Technical Details

This workflow consists of 4 nodes that work together to automate your process. Here's what it uses:

- @n8n/n8n-nodes-langchain.chatTrigger: When chat message received
- @n8n/n8n-nodes-langchain.lmChatGoogleGemini: Flash 2.0
- @n8n/n8n-nodes-langchain.toolWorkflow: Story Agent
- @n8n/n8n-nodes-langchain.agent: Parent Agent

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

