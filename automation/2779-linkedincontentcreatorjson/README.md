# LinkedIn_Content_Creator.json

Categories: Data Management

This workflow lets you click Test workflow to grab the next “To Do” topic from your LinkedIn-Posts Google Sheet, gather three recent articles with Tavily, and have Claude-3.5 Sonnet fuse their insights into a sub-700-character, hashtag-rich LinkedIn post. The finished post is written back to the sheet and the row’s status is flipped to Created, so it’s ready for review or scheduling.

## Technical Details

This workflow consists of 7 nodes that work together to automate your process. Here's what it uses:

- stickyNote: Sticky Note
- manualTrigger: When clicking ‘Test workflow’
- googleSheets: Get Topic, Send Content
- httpRequest: Tavily
- @n8n/n8n-nodes-langchain.lmChatOpenRouter: OpenRouter Chat Model
- @n8n/n8n-nodes-langchain.agent: Content Creator

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

