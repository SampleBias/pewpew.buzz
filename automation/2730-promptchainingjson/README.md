# Prompt_Chaining.json

Categories: Content Creation

Prompt Chaining uses a structured multi-agent flow to transform a chat input into a polished blog post. It generates an outline, improves it, expands it into content, and automatically posts to Google Docs.

## Technical Details

This workflow consists of 10 nodes that work together to automate your process. Here's what it uses:

- @n8n/n8n-nodes-langchain.lmChatOpenAi: 4o mini
- @n8n/n8n-nodes-langchain.agent: Outline Writer, Outline Evaluation, Blog Writer
- stickyNote: Sticky Note
- googleDocs: Post to Docs
- @n8n/n8n-nodes-langchain.lmChatDeepSeek: DeepSeek R1
- @n8n/n8n-nodes-langchain.chatTrigger: When chat message received
- @n8n/n8n-nodes-langchain.lmChatGoogleGemini: 2.0 Flash
- @n8n/n8n-nodes-langchain.lmChatAnthropic: Claude 3.5

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

