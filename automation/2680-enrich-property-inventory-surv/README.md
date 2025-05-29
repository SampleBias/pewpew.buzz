# Enrich Property Inventory Survey with Image Recognition and AI Agent

Categories: AI, Customer Support, Ecommerce

Enrich Property Inventory Survey with Image Recognition and AI Agent

## Technical Details

This workflow consists of 29 nodes that work together to automate your process. Here's what it uses:

- manualTrigger: When clicking "Test workflow"
- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model1
- airtable: Get Applicable Rows, Enrich Product Rows
- executeWorkflowTrigger: Execute Workflow Trigger
- set: Edit Fields, Fallback Response, Reverse Image Search Response, Firecrawl Scrape Success Response, Firecrawl scrape Error Response
- httpRequest: SERP Google Reverse Image API, Firecrawl Scrape API
- @n8n/n8n-nodes-langchain.toolWorkflow: Reverse Image Search Tool, Firecrawl Web Scaper Tool
- if: Scrape Success?
- @n8n/n8n-nodes-langchain.outputParserStructured: Structured Output Parser
- stickyNote: Sticky Note, Sticky Note1, Sticky Note2, Sticky Note3, Sticky Note4, Sticky Note6, Sticky Note5, Sticky Note7, Sticky Note8, Sticky Note9
- @n8n/n8n-nodes-langchain.openAi: Analyse Image
- @n8n/n8n-nodes-langchain.agent: Object Identifier Agent
- switch: Actions Router

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

