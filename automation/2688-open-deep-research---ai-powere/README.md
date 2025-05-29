# Open Deep Research - AI-Powered Autonomous Research Workflow

Categories: AI, Analytics, Education

Open Deep Research - AI-Powered Autonomous Research Workflow

## Technical Details

This workflow consists of 17 nodes that work together to automate your process. Here's what it uses:

- @n8n/n8n-nodes-langchain.chatTrigger: Chat Message Trigger
- @n8n/n8n-nodes-langchain.chainLlm: Generate Search Queries using LLM
- @n8n/n8n-nodes-langchain.lmChatOpenRouter: LLM Response Provider (OpenRouter)
- code: Parse and Chunk JSON Data, Format SerpAPI Organic Results
- httpRequest: Perform SerpAPI Search Request, Perform Jina AI Analysis Request
- @n8n/n8n-nodes-langchain.agent: Extract Relevant Context via LLM, Generate Comprehensive Research Report
- splitInBatches: Split Data for SerpAPI Batching, Split Data for Jina AI Batching
- @n8n/n8n-nodes-langchain.memoryBufferWindow: LLM Memory Buffer (Input Context), LLM Memory Buffer (Report Context)
- @n8n/n8n-nodes-langchain.toolWikipedia: Fetch Wikipedia Information
- stickyNote: Sticky Note: SerpAPI Setup, Sticky Note: Jina AI Setup, Sticky Note: OpenRouter API Setup

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

