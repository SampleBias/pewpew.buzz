# Calendar_Agent_Demo.json

Categories: Project Management

The Calendar Agent Demo workflow allows users to manage their Google Calendar using natural language, enabling them to create events (with or without attendees) or retrieve upcoming schedules. Powered by AI, it intelligently interprets user intent and executes the appropriate calendar action automatically.

## Technical Details

This workflow consists of 7 nodes that work together to automate your process. Here's what it uses:

- executeWorkflowTrigger: Execute Workflow Trigger
- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model
- googleCalendarTool: Create Event, Create Event with Attendee, Get Events
- set: Response
- @n8n/n8n-nodes-langchain.agent: Calendar Agent

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

