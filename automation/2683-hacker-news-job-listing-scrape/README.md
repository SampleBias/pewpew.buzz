# Hacker News Job Listing Scraper and Parser

Categories: AI, Content Creation, Education

Hacker News Job Listing Scraper and Parser

## Technical Details

This workflow consists of 20 nodes that work together to automate your process. Here's what it uses:

- manualTrigger: When clicking ‘Test workflow’
- stickyNote: Sticky Note, Sticky Note1, Sticky Note2, Sticky Note3, Sticky Note4
- splitOut: Split Out, Split out children (jobs)
- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model
- @n8n/n8n-nodes-langchain.outputParserStructured: Structured Output Parser
- httpRequest: Search for Who is hiring posts, HI API: Get the individual job post, HN API: Get Main Post
- set: Get relevant data, Extract text
- filter: Get latest post
- @n8n/n8n-nodes-langchain.chainLlm: Trun into structured data
- code: Clean text
- limit: Limit for testing (optional)
- airtable: Write results to airtable

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

