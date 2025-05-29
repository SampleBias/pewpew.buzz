# __Content_Creator_Agent.json

Categories: Content Creation

This agent generates SEO-optimized, well-structured blog posts in HTML based on user-provided topics by leveraging Tavily for real-time research and an Anthropic AI model for writing. If successful, it returns a polished HTML blog; otherwise, it gracefully handles errors with a fallback message.

## Technical Details

This workflow consists of 6 nodes that work together to automate your process. Here's what it uses:

- @n8n/n8n-nodes-langchain.toolHttpRequest: Tavily
- @n8n/n8n-nodes-langchain.agent: Content Creator Agent
- @n8n/n8n-nodes-langchain.lmChatAnthropic: Anthropic Chat Model
- set: Response, Try Again
- executeWorkflowTrigger: When Executed by Another Workflow

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

