# ___Scrape_Demo.json

Categories: Email

The 🛠️Scrape Demo workflow performs automated email scraping from search results. It takes a location-based query, fetches Google Maps search result pages, extracts all URLs, filters and deduplicates them, scrapes each page’s content, extracts email addresses (excluding images), deduplicates the results again, and logs the final email list into a Google Sheet.

## Technical Details

This workflow consists of 13 nodes that work together to automate your process. Here's what it uses:

- code: Code, Code1
- filter: Filter
- removeDuplicates: Remove Duplicates, Remove Duplicates1
- httpRequest: HTTP Request1, HTTP Request
- splitInBatches: Loop Over Items, Loop Over Items1
- googleSheets: Google Sheets
- aggregate: Aggregate
- executeWorkflowTrigger: Execute Workflow Trigger
- splitOut: Split Out

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

