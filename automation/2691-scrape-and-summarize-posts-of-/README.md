# Scrape and summarize posts of a news site without RSS feed using AI and save them to a NocoDB

Categories: AI, Marketing, Content Creation

Scrape and summarize posts of a news site without RSS feed using AI and save them to a NocoDB

## Technical Details

This workflow consists of 36 nodes that work together to automate your process. Here's what it uses:

- html: Extract the HTML with the right css class, Extract date, Extract individual posts
- openAi: Summary, Keywords
- set: Rename keywords, Rename Summary
- merge: Merge, Merge date & links, Merge Content with Date & Link, Merge ChatGPT output with Date & Link
- code: Select posts of last 7 days
- httpRequest: HTTP Request1, Retrieve the web page for further processsing
- stickyNote: Sticky Note, Sticky Note1, Sticky Note2, Sticky Note3, Sticky Note4, Sticky Note5, Sticky Note6, Sticky Note7, Sticky Note9, Sticky Note10, Sticky Note11, Sticky Note12, Sticky Note13, Sticky Note14, Sticky Note15, Sticky Note16, Sticky Note17, Sticky Note18
- scheduleTrigger: Schedule Trigger each week
- nocoDb: NocoDB news database
- itemLists: Create single link items, Create single date items

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

