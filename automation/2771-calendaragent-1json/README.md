# __Calendar_Agent (1).json

Categories: Data Management, Project Management

This AI-powered workflow turns plain-language instructions into Google Calendar actions—creating, updating, fetching, or deleting events with the right node. It routes the request through GPT-4o, executes the chosen calendar tool, then returns a success message or a fallback error prompt.

## Technical Details

This workflow consists of 10 nodes that work together to automate your process. Here's what it uses:

- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model
- set: Try Again, Success
- @n8n/n8n-nodes-langchain.agent: Calendar Agent
- googleCalendarTool: Create Event with Attendee, Create Event, Get Events, Delete Event, Update Event
- executeWorkflowTrigger: When Executed by Another Workflow

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

