# LLM_Testing.json

Categories: AI

This workflow listens for an incoming chat, then lets three different LLM agents (GPT-4o, Claude 3.5 Sonnet, and Gemini Flash 2.0) query a Pinecone vector store (“nvidia”) via the nvidia tool to retrieve embedded earnings-report passages.
Each agent summarizes the requested NVIDIA financial metric and returns a concise answer, giving you an easy way to compare model responses against the same up-to-date data source.

## Technical Details

This workflow consists of 19 nodes that work together to automate your process. Here's what it uses:

- @n8n/n8n-nodes-langchain.chatTrigger: When chat message received
- @n8n/n8n-nodes-langchain.toolVectorStore: nvidia, nvidia1, nvidia2
- @n8n/n8n-nodes-langchain.vectorStorePinecone: Pinecone Vector Store, Pinecone Vector Store1, Pinecone Vector Store2
- @n8n/n8n-nodes-langchain.embeddingsOpenAi: Embeddings OpenAI1, Embeddings OpenAI, Embeddings OpenAI2
- @n8n/n8n-nodes-langchain.lmChatOpenAi: GPT-4o, GPT-4o_
- @n8n/n8n-nodes-langchain.lmChatAnthropic: Claude 3.5 Sonnet, Claude 3.5 Sonnet_
- @n8n/n8n-nodes-langchain.agent: GPT-4o Agent, Claude 3.5 Sonnet Agent, GPT-4o Agent1
- @n8n/n8n-nodes-langchain.lmChatGoogleGemini: Gemini Flash 2.0, Gemini Flash 2.0_

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

