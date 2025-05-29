# __Personal_Assistant.json

Categories: Data Management, Email

It will pull information from a database, send emails, and calendar events

## Technical Details

This workflow consists of 14 nodes that work together to automate your process. Here's what it uses:

- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model, OpenAI Chat Model1
- @n8n/n8n-nodes-langchain.toolVectorStore: Vector Store Tool
- @n8n/n8n-nodes-langchain.embeddingsOpenAi: Embeddings OpenAI
- @n8n/n8n-nodes-langchain.vectorStorePinecone: Pinecone Vector Store
- @n8n/n8n-nodes-langchain.toolWorkflow: ⚙️Get Emails, ⚙️Send Email, ⚙️Get Calendar, ⚙️Set Calendar Event, ⚙️Update Database, ⚙️Summarize Database
- telegramTrigger: Telegram Trigger
- telegram: Telegram
- @n8n/n8n-nodes-langchain.agent: AI Personal Assistant

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

