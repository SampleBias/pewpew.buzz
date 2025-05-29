# Email support

Categories: Email

The workflow auto-detects customer-support emails, drafts friendly replies using your FAQ knowledge base, and sends them back while tagging the original thread. Non-support messages are ignored so only relevant emails get an AI response.

## Technical Details

This workflow consists of 11 nodes that work together to automate your process. Here's what it uses:

- stickyNote: Sticky Note
- gmailTrigger: Gmail Trigger
- @n8n/n8n-nodes-langchain.textClassifier: Text Classifier
- @n8n/n8n-nodes-langchain.lmChatOpenRouter: OpenRouter Chat Model
- noOp: No Operation, do nothing
- @n8n/n8n-nodes-langchain.agent: AI Agent
- @n8n/n8n-nodes-langchain.vectorStorePinecone: Pinecone Vector Store
- @n8n/n8n-nodes-langchain.embeddingsOpenAi: Embeddings OpenAI
- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model
- gmail: Label, Send

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

