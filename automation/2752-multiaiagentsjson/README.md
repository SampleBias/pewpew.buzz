# Multi_AI_Agents.json

Categories: AI, Content Creation

This workflow automatically generates content for blog posts, LinkedIn, and X (Twitter) by using multiple AI agents that respond to new entries in a Google Sheet. It pulls relevant online information using Tavily, splits and aggregates the data, then sends AI-crafted outputs to update the corresponding campaign record in Google Sheets.

## Technical Details

This workflow consists of 12 nodes that work together to automate your process. Here's what it uses:

- aggregate: Aggregate
- splitOut: Split Out
- httpRequest: Search Internet
- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model1, OpenAI Chat Model2, OpenAI Chat Model
- googleSheets: Update Campaign
- googleSheetsTrigger: Google Sheets Trigger
- set: Set Search Fields
- @n8n/n8n-nodes-langchain.agent: Blog Writer, LinkedIn, X

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

