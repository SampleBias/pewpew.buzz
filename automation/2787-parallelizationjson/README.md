# Parallelization.json

Categories: AI

This n8n workflow implements parallelized text analysis using three AI agents—Emotion, Intent, and Bias—to assess incoming chat messages simultaneously. Their individual outputs are merged, aggregated, and structured into a final summary report, which is automatically written to a Google Doc, enabling scalable, multi-dimensional NLP evaluations.

## Technical Details

This workflow consists of 13 nodes that work together to automate your process. Here's what it uses:

- stickyNote: Sticky Note
- @n8n/n8n-nodes-langchain.agent: Emotion Agent, Intent Agent, Bias Agent, Final Agent
- @n8n/n8n-nodes-langchain.chatTrigger: When chat message received
- merge: Merge, Merge1
- aggregate: Aggregate
- googleDocs: Write to Docs
- @n8n/n8n-nodes-langchain.lmChatDeepSeek: DeepSeek R1
- @n8n/n8n-nodes-langchain.lmChatOpenAi: 4o mini, 4o_mini

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

