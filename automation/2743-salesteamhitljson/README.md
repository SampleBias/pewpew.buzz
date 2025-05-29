# Sales_Team___HITL.json

Categories: Email

To create a high-quality, personalized sales email pipeline for incoming Airtable leads, enhanced by AI but controlled by human feedback.

## Technical Details

This workflow consists of 13 nodes that work together to automate your process. Here's what it uses:

- airtableTrigger: Airtable Trigger
- @n8n/n8n-nodes-langchain.lmChatAnthropic: Anthropic Chat Model
- airtableTool: Project Database
- @n8n/n8n-nodes-langchain.agent: Sales Agent, Revision Agent
- @n8n/n8n-nodes-langchain.outputParserStructured: Structured Output Parser
- gmail: Send Email, Get Feedback
- @n8n/n8n-nodes-langchain.lmChatGoogleGemini: Google Gemini Chat Model
- set: Set Email
- @n8n/n8n-nodes-langchain.textClassifier: Check Feedback
- stickyNote: Sticky Note, Sticky Note1

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

