# DeepSeek_R1_Planning_Agents.json

Categories: Email, Project Management

he DeepSeek R1 Planning Agents n8n workflow you’ve built is an intelligent multi-agent system designed for task planning, step breakdown, and automated execution using DeepSeek models, OpenAI, and integrated tools like Gmail and Google Calendar.

## Technical Details

This workflow consists of 23 nodes that work together to automate your process. Here's what it uses:

- @n8n/n8n-nodes-langchain.chatTrigger: When chat message received
- @n8n/n8n-nodes-langchain.memoryBufferWindow: Window Buffer Memory
- @n8n/n8n-nodes-langchain.agent: AI Agent, DeepSeek Planner, Tools Agent, Tools Agent1
- @n8n/n8n-nodes-langchain.lmChatOpenAi: DeepSeek R1 Model, OpenRouter DeepSeek R1, DeepSeek V3 Model, DeepSeek R1 Model1, GPT-4o Mini, GPT-4o Mini1
- stickyNote: Sticky Note1, Sticky Note2, Sticky Note
- gmailTool: Send Email, Send Email Tool, Send Email Tool1
- googleCalendarTool: Create Event, Create Event1
- set: Response, Response1
- httpRequest: DeepSeek R1 Planner

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

