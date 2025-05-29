# Make OpenAI Citation for File Retrieval RAG

Categories: AI, Data Management, Dev Ops

Make OpenAI Citation for File Retrieval RAG

## Technical Details

This workflow consists of 19 nodes that work together to automate your process. Here's what it uses:

- aggregate: Aggregate
- @n8n/n8n-nodes-langchain.memoryBufferWindow: Window Buffer Memory
- stickyNote: Sticky Note4, Sticky Note, Sticky Note1, Sticky Note2, Sticky Note3, Sticky Note5, Sticky Note6
- @n8n/n8n-nodes-langchain.chatTrigger: Create a simple Trigger to have the Chat button within N8N
- @n8n/n8n-nodes-langchain.openAi: OpenAI Assistant with Vector Store
- httpRequest: Get ALL Thread Content, Retrieve file name from a file ID
- splitOut: Split all message iterations from a thread, Split all content from a single message, Split all citations from a single message
- set: Regularize output
- markdown: Optional Markdown to HTML
- code: Finnaly format the output

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

