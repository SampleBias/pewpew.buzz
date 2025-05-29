# Visual Regression Testing with Apify and AI Vision Model

Categories: AI, Education, Engineering

Visual Regression Testing with Apify and AI Vision Model

## Technical Details

This workflow consists of 34 nodes that work together to automate your process. Here's what it uses:

- googleDrive: Base Image, Upload to Drive
- @n8n/n8n-nodes-langchain.lmChatGoogleGemini: Google Gemini Chat Model
- @n8n/n8n-nodes-langchain.outputParserStructured: Structured Output Parser
- stickyNote: Sticky Note, Sticky Note1, Sticky Note2, Sticky Note3, Sticky Note4, Sticky Note5, Sticky Note6, Sticky Note7, Sticky Note8, Sticky Note9
- splitInBatches: Loop Over Items, For Each Webpage...
- wait: Wait, Wait1
- httpRequest: Download Screenshot, Run Webpage Screenshot, Run Webpage Screenshot1, Download New Screenshot
- googleSheets: Update Base Image, Get URLs with Missing Base Images, Get Webpages List
- merge: Merge, Combine Screenshots
- scheduleTrigger: Schedule Trigger
- filter: Has Changes
- set: Combine Row and Result
- aggregate: Aggregate
- linear: Create Report
- manualTrigger: When clicking ‘Test workflow’
- @n8n/n8n-nodes-langchain.chainLlm: Visual Regression Agent

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

