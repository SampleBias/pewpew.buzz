# Famous_Brands_Shorts_Template.json

Categories: Content Creation

This end-to-end workflow turns each spreadsheet row into a “tiny branded building” short: GPT drafts image, video, and music prompts, Fal-AI renders the visuals, ElevenLabs creates the soundtrack, and Creatomate stitches everything together. Once the vertical clip is ready, it’s uploaded to Drive, posted to YouTube, TikTok, and Instagram via Blotato, and the Google Sheet is updated—all hands-free.

## Technical Details

This workflow consists of 44 nodes that work together to automate your process. Here's what it uses:

- stickyNote: Sticky Note9, Sticky Note1, Sticky Note8, Sticky Note5, Sticky Note4, Sticky Note3, Sticky Note2, Sticky Note, Sticky Note7, Sticky Note6, Sticky Note10
- wait: 60 Seconds, 10 Seconds, 20 Seconds, 3 Seconds, 5 Minutes, 12 Seconds
- @n8n/n8n-nodes-langchain.lmChatOpenRouter: GPT 4.1
- aggregate: Aggregate
- set: Grab Elements, Set Brands
- httpRequest: YouTube, TikTok, Instagram, Upload to Blotato, Download Video, Render Video, Generate Audio, Get Videos, Get Video Status, Generate Videos, Get Images, Get Status, Generate Images
- googleSheets: Google Sheets, Get Story
- googleDrive: Share File, Upload to Drive
- if: Images Done?, Videos Done?
- @n8n/n8n-nodes-langchain.outputParserStructured: Prompts
- splitOut: Split Out
- @n8n/n8n-nodes-langchain.agent: Prompt Generator
- scheduleTrigger: Schedule Trigger

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

