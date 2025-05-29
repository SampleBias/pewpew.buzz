# Routing.json

Categories: Marketing, Email, Customer Support

This email routing system automatically classifies incoming Gmail messages into categories like High Priority, Customer Support, Promotions, and Finance/Billing using an AI text classifier. Based on classification, each email is processed by a specialized AI agent or escalated via Telegram for urgent human review.

## Technical Details

This workflow consists of 14 nodes that work together to automate your process. Here's what it uses:

- stickyNote: Sticky Note
- gmailTrigger: Gmail Trigger
- gmail: High Priority, Customer Support, Promotion, Finance/Billing
- @n8n/n8n-nodes-langchain.textClassifier: Email Classifier
- @n8n/n8n-nodes-langchain.lmChatOpenAi: 4o mini
- @n8n/n8n-nodes-langchain.agent: High Priority Agent, Customer Support Agent, Promotion Agent, Finance Agent
- telegramTool: Telegram
- gmailTool: Email Draft

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

