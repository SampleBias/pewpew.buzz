# Human_in_the_Loop_Calendar_Agent.json

Categories: Project Management

This Human-in-the-Loop Calendar Agent intelligently interprets Telegram queries to manage events with manual confirmation built into the flow. It uses intent detection, contact lookup, and calendar tools, then prompts a human for feedback before finalizing actions like creating, updating, or deleting events.

## Technical Details

This workflow consists of 17 nodes that work together to automate your process. Here's what it uses:

- telegramTrigger: Telegram Trigger
- @n8n/n8n-nodes-langchain.agent: Intent Agent, Correction Agent, Calendar Agent
- googleCalendarTool: Get_Events, Create Event, Create Event with Attendee, Update Event, Get Events, Delete Event
- airtableTool: Contacts
- @n8n/n8n-nodes-langchain.lmChatOpenAi: 4o mini
- set: Set Intent
- telegram: HITL, Response
- @n8n/n8n-nodes-langchain.textClassifier: Check Feedback
- stickyNote: Sticky Note

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

