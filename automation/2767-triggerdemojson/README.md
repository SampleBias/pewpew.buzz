# ___Trigger_Demo.json

Categories: Data Management

When you hit Test, the workflow grabs the list of Google Maps queries in the Manual Trigger’s JSON, then iterates through them with Loop Over Items. For each query it launches the separate 🛠️Scrape Demo workflow, waits three seconds to avoid overlap, and repeats until every query has been processed.

## Technical Details

This workflow consists of 5 nodes that work together to automate your process. Here's what it uses:

- splitInBatches: Loop Over Items
- executeWorkflow: Execute Workflow
- wait: Wait
- manualTrigger: When clicking ‘Test workflow’
- stickyNote: Sticky Note

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

