# Outlook_Inbox_Manager.json

Categories: Email

This automation monitors a Microsoft Outlook inbox and uses AI to clean up incoming emails, classify them by type (High Priority, Billing, Promotion), and move them into appropriate folders. It also drafts billing replies, sends polite declines for promotions, and pushes urgent notifications to Telegram for real-time attention.

## Technical Details

This workflow consists of 17 nodes that work together to automate your process. Here's what it uses:

- microsoftOutlookTrigger: Microsoft Outlook Trigger
- @n8n/n8n-nodes-langchain.openAi: Clean Email
- @n8n/n8n-nodes-langchain.textClassifier: Text Classifier
- @n8n/n8n-nodes-langchain.lmChatGoogleGemini: Flash 2.0
- microsoftOutlook: High Priority Folder, Billing Folder, Promotion Folder
- @n8n/n8n-nodes-langchain.agent: Billing Agent, Promotion Agent
- microsoftOutlookTool: Create Draft, Send Email
- telegram: High Priority Notification, Billing Notification
- @n8n/n8n-nodes-langchain.lmChatOpenAi: 4o mini
- stickyNote: Sticky Note, Sticky Note1, Sticky Note2

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

