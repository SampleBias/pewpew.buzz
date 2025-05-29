# __Get_Calendar.json

Categories: Project Management

This workflow extracts a user's intended date from a natural language query, fetches calendar events for that day, summarizes each event using GPT, and compiles a response summarizing the day.

## Technical Details

This workflow consists of 7 nodes that work together to automate your process. Here's what it uses:

- googleCalendar: Google Calendar
- set: Edit Fields, Edit Fields1
- aggregate: Aggregate
- @n8n/n8n-nodes-langchain.openAi: Summarize Calendar, Find Current Date
- executeWorkflowTrigger: Execute Workflow Trigger

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

