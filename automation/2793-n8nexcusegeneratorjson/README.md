# n8n_Excuse_Generator.json

Categories: Webhooks

The n8n Excuse Generator workflow receives a problem and desired tone via a webhook, uses GPT-4o-mini to generate a clever excuse tailored to that tone, and sends the result back through a webhook response. It supports tones like realistic, funny, ridiculous, and outrageous, returning a concise, humorous excuse in 1–3 sentences.

## Technical Details

This workflow consists of 5 nodes that work together to automate your process. Here's what it uses:

- webhook: Webhook
- @n8n/n8n-nodes-langchain.agent: AI Agent
- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model
- respondToWebhook: Respond to Webhook
- stickyNote: Sticky Note1

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

