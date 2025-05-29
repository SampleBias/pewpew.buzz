# Log_Agent_Outputs.json

Categories: Data Management

Captures every Telegram request handled by the GPT-4.1-mini agent—along with its tool calls, token usage, and cost—then writes the details to a Google Sheets log.
Sends the agent’s reply or an error notice back to the user while preserving full audit data for each run.

## Technical Details

This workflow consists of 21 nodes that work together to automate your process. Here's what it uses:

- @n8n/n8n-nodes-langchain.lmChatOpenRouter: 4.1-mini
- gmailTool: Send Email
- airtableTool: Get Contacts
- googleSheets: Log, Errors
- googleCalendarTool: Create Event
- code: Clean Up, Clean_Up
- telegramTrigger: Telegram Trigger
- telegram: Error Response, Response
- stickyNote: Sticky Note, Sticky Note1, Sticky Note2, Sticky Note3, Sticky Note4, Sticky Note5, Sticky Note6, Sticky Note7, Sticky Note8
- @n8n/n8n-nodes-langchain.agent: AI Agent

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

