# Firecrawl_Extract_Template.json

Categories: Data Management

This n8n workflow uses Firecrawl's API to extract structured quote and author data from a dynamic list of URLs (e.g. quotes.toscrape.com). It includes a retry loop with a 30-second initial wait and a conditional 10-second retry if no data is returned, making it ideal for asynchronous extraction tasks where delayed results are expected.

## Technical Details

This workflow consists of 9 nodes that work together to automate your process. Here's what it uses:

- manualTrigger: When clicking ‘Test workflow’
- httpRequest: Extract, Get Results
- if: If
- wait: 30 Secs, 10 Seconds
- stickyNote: Sticky Note, Sticky Note1
- set: Edit Fields

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

