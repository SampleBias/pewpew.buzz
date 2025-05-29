# __Research_Agent.json

Categories: AI

our Research Agent is well-designed with a logical fallback strategy: Wikipedia → Hacker News → SerpAPI. It efficiently answers queries using prioritized sources and structured output handling.

## Technical Details

This workflow consists of 8 nodes that work together to automate your process. Here's what it uses:

- executeWorkflowTrigger: Execute Workflow Trigger
- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model
- set: Try Again, Success
- @n8n/n8n-nodes-langchain.toolSerpApi: SerpAPI
- @n8n/n8n-nodes-langchain.toolWikipedia: Wikipedia
- hackerNewsTool: Hacker News
- @n8n/n8n-nodes-langchain.agent: Research Agent

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

