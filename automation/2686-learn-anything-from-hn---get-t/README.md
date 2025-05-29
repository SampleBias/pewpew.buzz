# Learn Anything from HN - Get Top Resource Recommendations from Hacker News

Categories: AI, Content Creation

Learn Anything from HN - Get Top Resource Recommendations from Hacker News

## Technical Details

This workflow consists of 10 nodes that work together to automate your process. Here's what it uses:

- @n8n/n8n-nodes-langchain.lmChatGoogleGemini: Google Gemini Chat Model
- @n8n/n8n-nodes-langchain.chainLlm: Basic LLM Chain
- hackerNews: SearchAskHN
- httpRequest: FindHNComments
- aggregate: CombineIntoSingleText
- splitOut: SplitOutChildrenIDs
- formTrigger: GetTopicFromToLearn
- emailSend: SendEmailWithTopResources
- markdown: Convert2HTML
- noOp: Finished

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

