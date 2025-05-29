# ___Inbox_Management_Agent.json

Categories: Email

This agent checks your Gmail inbox every minute, uses GPT-4o to classify each unread email into High Priority, Customer Support, Promotions, or Finance/Billing, and automatically applies the matching label. Depending on the category, it then drafts an executive reply, sends a customer-service response, produces a promo summary with recommendations, or forwards a concise finance summary to accounting.

## Technical Details

This workflow consists of 14 nodes that work together to automate your process. Here's what it uses:

- gmailTrigger: Gmail Trigger
- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model
- gmail: High Priority, Customer Support, Promotion, Finance/Billing, Draft, Auto Reply, Send to Finance Dept
- @n8n/n8n-nodes-langchain.openAi: Creating Draft, Creating Email, Summary & Rec, Summary for Finance Dept
- @n8n/n8n-nodes-langchain.textClassifier: Text Classifier

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

