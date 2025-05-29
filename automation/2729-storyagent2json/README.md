# Story_Agent__2.json

Categories: Content Creation

Story Agent #2 receives setting, mainCharacter, and adventure inputs and generates a short story using those details. If any input is missing, it returns an error message asking for complete information.

## Technical Details

This workflow consists of 5 nodes that work together to automate your process. Here's what it uses:

- executeWorkflowTrigger: When Executed by Another Workflow
- @n8n/n8n-nodes-langchain.agent: Child Agent
- @n8n/n8n-nodes-langchain.lmChatGoogleGemini: Flash 2.0
- if: All Parameters Given?
- set: Try Again

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

