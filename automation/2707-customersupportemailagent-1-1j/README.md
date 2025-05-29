# __Customer_Support_Email_Agent (1) (1).json

Categories: Customer Support

This agent does email support by sending emails 

## Technical Details

This workflow consists of 13 nodes that work together to automate your process. Here's what it uses:

- gmailTrigger: Gmail Trigger
- set: Set Content
- @n8n/n8n-nodes-langchain.openAi: Customer Support Eval
- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model, OpenAI Chat Model1
- @n8n/n8n-nodes-langchain.toolVectorStore: Vector Store Tool
- @n8n/n8n-nodes-langchain.embeddingsOpenAi: Embeddings OpenAI
- @n8n/n8n-nodes-langchain.vectorStorePinecone: Pinecone Vector Store
- gmailTool: createDraft
- @n8n/n8n-nodes-langchain.agent: Customer Support Agent
- telegram: Response, Response Not Customer Support
- switch: Customer Support?

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

