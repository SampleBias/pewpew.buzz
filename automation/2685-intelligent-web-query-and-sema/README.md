# Intelligent Web Query and Semantic Re-Ranking Flow using Brave and Google Gemini

Categories: AI, Content Creation

Intelligent Web Query and Semantic Re-Ranking Flow using Brave and Google Gemini

## Technical Details

This workflow consists of 20 nodes that work together to automate your process. Here's what it uses:

- stickyNote: Sticky Note4, Sticky Note, Sticky Note6, Sticky Note5
- dateTime: Date & Time
- webhook: Webhook
- @n8n/n8n-nodes-langchain.outputParserAutofixing: Auto-fixing Output Parser6, Auto-fixing Output Parser
- @n8n/n8n-nodes-langchain.outputParserStructured: Structured Output Parser1, Structured Output Parser2
- code: Query-1 Combined
- respondToWebhook: Respond to Webhook
- @n8n/n8n-nodes-langchain.chainLlm: Semantic Search - Result Re-Ranker, Semantic Search -Query Maker
- httpRequest: Query, Webhook Call
- @n8n/n8n-nodes-langchain.lmChatAnthropic: Anthropic Chat Model
- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model
- @n8n/n8n-nodes-langchain.lmChatGoogleGemini: Parser Model, Agent Model

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

