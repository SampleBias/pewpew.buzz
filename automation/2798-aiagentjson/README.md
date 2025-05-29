# AI_Agent.json

Categories: Email

The AI Agent workflow in n8n functions as an intelligent email assistant that listens to chat inputs, extracts email-related intents, retrieves recipient contact information (if needed), and sends well-formatted emails via Gmail. It leverages memory for conversation continuity, uses a Google Sheets-based contact database, and confirms each email's successful delivery to the user.

## Technical Details

This workflow consists of 7 nodes that work together to automate your process. Here's what it uses:

- @n8n/n8n-nodes-langchain.chatTrigger: When chat message received
- @n8n/n8n-nodes-langchain.agent: AI Agent
- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model
- @n8n/n8n-nodes-langchain.memoryBufferWindow: Window Buffer Memory
- gmailTool: sendEmail
- googleSheetsTool: contactDatabase
- set: Output

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

