# __Content_Creator_Agent (1).json

Categories: Content Creation

This Content Creator Agent workflow is designed to generate SEO-optimized, well-formatted HTML blog posts using AI. It uses a LangChain agent with Anthropic’s Claude model to write the blog, and Tavily to search the web for recent, relevant sources—ensuring all external citations are clickable, embedded in the content, and tailored to a clear, engaging structure.

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

