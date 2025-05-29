# HITL_Example_Flows.json

Categories: Data Management

This workflow turns a Telegram message into a fact-checked X post: GPT-4 (via OpenRouter) drafts a tweet after running a Tavily web search, then asks the human in Telegram to approve or revise it. A “yes” posts straight to X; any free-text feedback is classified, routed through a revision agent, and looped back for another quick approval cycle—keeping a human firmly in the loop.

## Technical Details

This workflow consists of 34 nodes that work together to automate your process. Here's what it uses:

- telegramTrigger: Telegram Trigger, Telegram_Trigger
- @n8n/n8n-nodes-langchain.toolHttpRequest: Tavily, Tavily Search
- telegram: Submit Approval, Request Feedback, Denial message
- if: If
- twitter: X, X Post
- @n8n/n8n-nodes-langchain.lmChatOpenRouter: GPT 4.1, GPT_4.1, 2.0 Flash
- @n8n/n8n-nodes-langchain.textClassifier: Text Classifier
- @n8n/n8n-nodes-langchain.agent: Revision Agent, X Post Agent, X_Post Agent
- set: Set Post
- stickyNote: Sticky Note, Sticky Note1, Sticky Note2, Sticky Note3, Sticky Note4, Sticky Note5, Sticky Note6, Sticky Note7, Sticky Note8, Sticky Note9, Sticky Note10, Sticky Note11, Sticky Note12, Sticky Note13, Sticky Note14, Sticky Note15

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

