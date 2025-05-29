# __Invoice_Agent.json

Categories: Data Management

This Telegram-integrated automation extracts invoice data from uploaded image files using OCR, parses key details like total amount, due date, and notes, and appends them to a Google Sheets invoice database. It also stores the invoice file in Google Drive and replies with a clear, AI-generated summary and access link for easy tracking.

## Technical Details

This workflow consists of 12 nodes that work together to automate your process. Here's what it uses:

- telegramTrigger: Telegram Trigger
- telegram: Download File, Telegram, Reply
- googleSheets: Update Database
- code: Parse Text
- httpRequest: Analyze Image
- set: Set
- googleDrive: Add Invoice Image to Drive
- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model
- @n8n/n8n-nodes-langchain.memoryBufferWindow: Window Buffer Memory
- @n8n/n8n-nodes-langchain.agent: Invoice Agent

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

