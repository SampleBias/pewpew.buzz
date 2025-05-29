# Voice_Email_Agent.json

Categories: Email, Webhooks

This workflow turns voice or text inputs into professional emails by retrieving contact info from Google Sheets and using GPT-4o to draft messages. It then sends the email through Gmail and responds via webhook

## Technical Details

This workflow consists of 6 nodes that work together to automate your process. Here's what it uses:

- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model
- respondToWebhook: Respond to Webhook
- googleSheetsTool: contactData
- gmailTool: sendEmail
- webhook: Webhook
- @n8n/n8n-nodes-langchain.agent: Email Agent

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

