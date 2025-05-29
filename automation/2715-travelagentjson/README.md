# Travel_Agent.json

Categories: Data Management, Email

It will 📥 Capture Request Parse Locations, Validate Dates, Convert Airports, Refine Inputs, Search Flights, Search Resorts, Search Activities, Use AI, Summarize Results, Write Email, Format HTML, Send Plan, Confirm Response

## Technical Details

This workflow consists of 15 nodes that work together to automate your process. Here's what it uses:

- webhook: Webhook
- respondToWebhook: Respond to Webhook
- set: Set Fields, Response
- @n8n/n8n-nodes-langchain.chainLlm: Airport Codes & Dates
- @n8n/n8n-nodes-langchain.lmChatOpenAi: 4o
- @n8n/n8n-nodes-langchain.outputParserStructured: Locations & Dates, Subject & Email
- httpRequest: Flights, Resorts, Activities
- @n8n/n8n-nodes-langchain.agent: Email Agent
- @n8n/n8n-nodes-langchain.lmChatAnthropic: Claude 3.5
- gmail: Send Plan
- stickyNote: Sticky Note

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

