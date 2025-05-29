# Extract insights & analyse YouTube comments via AI Agent chat

Categories: AI, Analytics, Marketing

Extract insights & analyse YouTube comments via AI Agent chat

## Technical Details

This workflow consists of 29 nodes that work together to automate your process. Here's what it uses:

- stickyNote: Sticky Note9, Sticky Note7, Sticky Note6, Sticky Note, Sticky Note1, Sticky Note2, Sticky Note3
- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model
- @n8n/n8n-nodes-langchain.toolWorkflow: get_channel_details, get_video_description, get_list_of_videos, get_list_of_comments, search, analyze_thumbnail, video_transcription
- @n8n/n8n-nodes-langchain.memoryPostgresChat: Postgres Chat Memory
- @n8n/n8n-nodes-langchain.agent: AI Agent
- @n8n/n8n-nodes-langchain.chatTrigger: When chat message received
- httpRequest: Get Comments, Get Channel Details, Get Video Description, Run Query, Get Videos by Channel, Get Video Transcription
- executeWorkflowTrigger: Execute Workflow Trigger
- set: Edit Fields, Response
- switch: Switch
- @n8n/n8n-nodes-langchain.openAi: OpenAI

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

