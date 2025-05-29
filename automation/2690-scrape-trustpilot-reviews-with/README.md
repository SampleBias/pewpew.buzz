# Scrape Trustpilot Reviews with DeepSeek, Analyze Sentiment with OpenAI

Categories: AI, Marketing, Customer Support

Scrape Trustpilot Reviews with DeepSeek, Analyze Sentiment with OpenAI

## Technical Details

This workflow consists of 20 nodes that work together to automate your process. Here's what it uses:

- splitOut: Split Out
- @n8n/n8n-nodes-langchain.informationExtractor: Information Extractor
- if: If
- manualTrigger: When clicking ‘Test workflow’
- limit: Limit1
- stickyNote: Sticky Note, Sticky Note1, Sticky Note2, Sticky Note3
- set: Set Parameters
- httpRequest: Get reviews, Get Single review
- html: Extract, Extract review
- googleSheets: Get rows, Get Google Sheets, Update sheet
- @n8n/n8n-nodes-langchain.sentimentAnalysis: Sentiment Analysis
- @n8n/n8n-nodes-langchain.lmChatOpenAi: DeepSeek Chat Model, OpenAI Chat Model

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

