# Think_Agents.json

Categories: AI

This Think Agent system coordinates multiple AI models and tools to handle user queries intelligently by leveraging reasoning steps before acting. It uses sub-workflows like “quoter” and “availability,” integrates Claude, Gemini, and GPT models, and employs a “Think” tool to validate logic and responses before final output.

## Technical Details

This workflow consists of 38 nodes that work together to automate your process. Here's what it uses:

- @n8n/n8n-nodes-langchain.agent: Think Agent, Think Agent1, Think Agent2
- @n8n/n8n-nodes-langchain.chatTrigger: When chat message received
- @n8n/n8n-nodes-langchain.toolThink: Think, Think1, Think2
- @n8n/n8n-nodes-langchain.lmChatAnthropic: Claude 3.5 Sonnet, Claude 3.5 Sonnet1, Claude 3.5 Sonnet2
- stickyNote: Sticky Note, Sticky Note1, Sticky Note2, Sticky Note3, Sticky Note4, Sticky Note5, Sticky Note6, Sticky Note7, Sticky Note8, Sticky Note9, Sticky Note10, Sticky Note11, Sticky Note12
- @n8n/n8n-nodes-langchain.lmChatOpenAi: GPT 4.1, GPT-4.1, GPT-4.
- @n8n/n8n-nodes-langchain.vectorStorePinecone: knowlege_base
- @n8n/n8n-nodes-langchain.embeddingsOpenAi: Embeddings OpenAI
- gmailTool: Send Email
- airtableTool: Contacts
- @n8n/n8n-nodes-langchain.toolHttpRequest: Web Search
- @n8n/n8n-nodes-langchain.lmChatGoogleGemini: 2.0 Flash, 2.0 Flash1
- @n8n/n8n-nodes-langchain.toolWorkflow: quoter, availability
- executeWorkflowTrigger: When Executed by Another Workflow
- @n8n/n8n-nodes-langchain.openAi: Quoter, Availability

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

