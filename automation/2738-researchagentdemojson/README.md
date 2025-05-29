# Research_Agent_Demo.json

Categories: Education

This research agent intelligently selects the most efficient tool—Wikipedia, Hacker News, or SerpAPI—to answer a user’s question, ensuring that only one tool is used based on availability of relevant information. It then delivers a concise, research-backed response optimized for relevance and speed using OpenAI's language model.

## Technical Details

This workflow consists of 7 nodes that work together to automate your process. Here's what it uses:

- executeWorkflowTrigger: Execute Workflow Trigger
- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model
- @n8n/n8n-nodes-langchain.toolWikipedia: Wikipedia
- hackerNewsTool: Hacker News
- @n8n/n8n-nodes-langchain.toolSerpApi: SerpAPI
- set: Response
- @n8n/n8n-nodes-langchain.agent: Research Agent

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

