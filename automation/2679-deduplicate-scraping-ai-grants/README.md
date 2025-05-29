# Deduplicate Scraping AI Grants for Eligibility using AI

Categories: AI, Education, Project Management

Deduplicate Scraping AI Grants for Eligibility using AI

## Technical Details

This workflow consists of 24 nodes that work together to automate your process. Here's what it uses:

- splitOut: Grants to List
- httpRequest: Get Grant Details, AI Grants since Yesterday
- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model, OpenAI Chat Model1
- @n8n/n8n-nodes-langchain.informationExtractor: Summarize Synopsis, Eligibility Factors
- merge: Merge
- airtable: Save to Tracker, Get New Eligible Grants Today, Get Subscribers
- removeDuplicates: Only New Grants
- html: Generate Email
- scheduleTrigger: Everyday @ 9am, Everyday @ 8.30am
- stickyNote: Sticky Note, Sticky Note1, Sticky Note2, Sticky Note3, Sticky Note4, Sticky Note5, Sticky Note6, Sticky Note7
- gmail: Send Subscriber Email

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

