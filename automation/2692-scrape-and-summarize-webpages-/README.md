# Scrape and summarize webpages with AI

Categories: AI, Analytics, Education

Scrape and summarize webpages with AI

## Technical Details

This workflow consists of 15 nodes that work together to automate your process. Here's what it uses:

- manualTrigger: When clicking "Execute Workflow"
- httpRequest: Fetch essay list, Fetch essay texts
- html: Extract essay names, Extract title
- set: Clean up
- stickyNote: Sticky Note, Sticky Note1
- splitOut: Split out into items
- limit: Limit to first 3
- @n8n/n8n-nodes-langchain.documentDefaultDataLoader: Default Data Loader
- @n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter: Recursive Character Text Splitter
- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model1
- merge: Merge
- @n8n/n8n-nodes-langchain.chainSummarization: Summarization Chain

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

