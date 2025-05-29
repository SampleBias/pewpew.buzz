# DeepSeek_R1.json

Categories: AI

The DeepSeek R1 workflow in n8n demonstrates two methods of interfacing with the DeepSeek Reasoner model: one via HTTP POST and one through LangChain's model wrapper (lmChatOpenAi). It listens for chat messages, optionally uses memory for context, and can generate and return logical answers or jokes. The HTTP method uses a raw API call to DeepSeek, while the LangChain method integrates with n8n's AI Agent tools for more flexible, contextual interactions.

## Technical Details

This workflow consists of 10 nodes that work together to automate your process. Here's what it uses:

- @n8n/n8n-nodes-langchain.chatTrigger: When chat message received
- @n8n/n8n-nodes-langchain.memoryBufferWindow: Window Buffer Memory
- @n8n/n8n-nodes-langchain.agent: AI Agent
- set: Result, Set Query
- manualTrigger: When clicking ‘Test workflow’
- httpRequest: DeepSeek R1
- @n8n/n8n-nodes-langchain.lmChatOpenAi: DeepSeek R1 Model
- stickyNote: Sticky Note, Sticky Note1

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

