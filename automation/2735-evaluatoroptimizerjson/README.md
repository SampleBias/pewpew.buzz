# Evaluator_Optimizer.json

Categories: Content Creation

This workflow generates light, humorous biographies from user input, automatically evaluates them for key criteria (including presence of a quote and no emojis), and loops back for optimization if needed. Once the biography meets all requirements, it is pushed directly to Google Docs.

## Technical Details

This workflow consists of 10 nodes that work together to automate your process. Here's what it uses:

- stickyNote: Sticky Note
- @n8n/n8n-nodes-langchain.chatTrigger: When chat message received
- @n8n/n8n-nodes-langchain.lmChatOpenAi: 4o mini
- @n8n/n8n-nodes-langchain.agent: Biography Agent, Evaluator Agent, Optimizer Agent
- if: Evaluate
- googleDocs: Push to Docs
- set: Set Bio
- @n8n/n8n-nodes-langchain.lmChatDeepSeek: DeepSeek R1

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

