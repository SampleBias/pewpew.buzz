# Autonomous AI crawler

Categories: Data Management, Dev Ops

Autonomous AI crawler

## Technical Details

This workflow consists of 38 nodes that work together to automate your process. Here's what it uses:

- @n8n/n8n-nodes-langchain.toolWorkflow: Text, URLs
- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model
- @n8n/n8n-nodes-langchain.outputParserStructured: JSON Parser
- set: Map company name and website, Select company name and website, Set social media array, Set domain to path, Set domain (text), Add protocool to domain (text), Set response (text), Set domain (URL), Set response (URL), Add protocool to domain (URL)
- manualTrigger: Execute workflow
- supabase: Get companies, Insert new row
- merge: Merge all data
- markdown: Convert HTML to Markdown
- stickyNote: Sticky Note, Sticky Note1, Sticky Note2, Sticky Note3, Sticky Note4, Sticky Note5, Sticky Note6, Sticky Note7, Sticky Note8, Sticky Note9
- html: Retrieve URLs
- splitOut: Split out URLs
- removeDuplicates: Remove duplicated
- filter: Filter out invalid URLs, Filter out empty hrefs
- aggregate: Aggregate URLs
- httpRequest: Get website (text), Get website (URL)
- @n8n/n8n-nodes-langchain.agent: Crawl website

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

