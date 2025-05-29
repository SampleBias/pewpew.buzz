# __Personal_Assistant_AI_Agent_2_0.json

Categories: AI

This workflow turns Telegram messages into an intelligent “personal-assistant” conversation powered by GPT-4o; the agent can consult a company knowledge base, look up contacts, calculate, and delegate tasks to dedicated calendar, email, research, projects, and Slack sub-agents. It automatically executes the required tool calls (e.g., send an email, schedule an event, post to Slack) and replies back to you on Telegram with the outcome.

## Technical Details

This workflow consists of 15 nodes that work together to automate your process. Here's what it uses:

- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model, OpenAI Chat Model1
- slackTool: Send Slack Message
- @n8n/n8n-nodes-langchain.vectorStorePinecone: Pinecone Vector Store
- @n8n/n8n-nodes-langchain.embeddingsOpenAi: Embeddings OpenAI
- @n8n/n8n-nodes-langchain.toolVectorStore: Knowledge Base
- googleSheetsTool: Contacts Data
- @n8n/n8n-nodes-langchain.toolWorkflow: 🤖Calendar_Agent, 🤖Research_Agent, 🤖Projects_Agent, 🤖___Email_Agent
- telegram: Respond to Me
- telegramTrigger: Telegram Trigger
- @n8n/n8n-nodes-langchain.toolCalculator: Calculator
- @n8n/n8n-nodes-langchain.agent: Personal Assistant

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

