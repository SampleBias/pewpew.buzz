# __Calendar_Agent.json

Categories: Project Management

The 🤖Calendar Agent workflow acts as an intelligent assistant for managing Google Calendar events. It can create solo or attendee-based events, retrieve schedules, and delete or update events using AI-driven input parsing and decision routing, ensuring seamless automation of calendar operations.

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

