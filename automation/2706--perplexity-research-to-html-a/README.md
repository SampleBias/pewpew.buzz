#  Perplexity Research to HTML_ AI-Powered Content Creation

Categories: AI, Analytics, Content Creation

 Perplexity Research to HTML_ AI-Powered Content Creation

## Technical Details

This workflow consists of 47 nodes that work together to automate your process. Here's what it uses:

- stickyNote: Sticky Note, Sticky Note1, Sticky Note4, Sticky Note2, Sticky Note5, Sticky Note6, Sticky Note7, Sticky Note3, Sticky Note8
- @n8n/n8n-nodes-langchain.lmChatOpenAi: gpt-4o-mini, gpt-4o-mini1, gpt-4o-mini2, gpt-4o-mini5, gpt-4o-mini3
- @n8n/n8n-nodes-langchain.outputParserStructured: Structured Output Parser1
- webhook: Webhook
- respondToWebhook: Respond to Webhook
- telegram: Telegram, Telegram2
- @n8n/n8n-nodes-langchain.chainLlm: Basic LLM Chain, Improve Users Topic
- noOp: Do Nothing1, No Operation, do nothing, Do Nothing, Do Nothing2, Do Nothing3, Do Nothing4
- if: If2, If, If Topic Exists, If Topic, If Article, If HTML
- set: Prompts, Get Topic, Chat Id, Article, Contents, Chat Id1, Success Response, Error Response
- executeWorkflowTrigger: Execute Workflow Trigger
- @n8n/n8n-nodes-langchain.agent: Perplexity Topic Agent, Extract JSON, Create HTML Article
- @n8n/n8n-nodes-langchain.toolWorkflow: Call Perplexity Researcher
- httpRequest: Perplexity

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

