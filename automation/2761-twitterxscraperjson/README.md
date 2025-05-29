# Twitter_X_Scraper.json

Categories: Data Management

This workflow scrapes Twitter/X search results for the query “OpenAI,” paginating up to three batches via cursor and counting logic. Each tweet’s ID, text, engagement metrics, and timestamp are extracted and continuously appended to a Google Sheet for analysis.

## Technical Details

This workflow consists of 16 nodes that work together to automate your process. Here's what it uses:

- manualTrigger: When clicking ‘Test workflow’
- set: Counter, Set Count, Set Increase, Set Count and Cursor
- if: If
- code: Increase Count, Extract Info
- googleSheets: Add to Sheet
- noOp: No Operation, do nothing
- limit: Limit
- httpRequest: Get Tweets
- stickyNote: Sticky Note, Sticky Note2, Sticky Note1, Sticky Note3

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

