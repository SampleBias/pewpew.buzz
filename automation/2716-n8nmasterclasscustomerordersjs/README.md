# n8n_Masterclass__Customer_Orders.jsonv

Categories: Email, Customer Support

This bot monitors a Google Sheet for new customer orders, summarizes each one using GPT-4o, and emails the summary to the team. The email is branded as coming from the "Customer Success Team" and includes details like customer name, product, quantity, and order status.

## Technical Details

This workflow consists of 3 nodes that work together to automate your process. Here's what it uses:

- googleSheetsTrigger: Google Sheets Trigger
- gmail: Gmail
- @n8n/n8n-nodes-langchain.openAi: Summarize

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

