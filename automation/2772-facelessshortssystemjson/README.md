# Faceless_Shorts_System.json

Categories: Content Creation

This end-to-end workflow pulls an idea row from a Google Sheet, then auto-generates themed animal images, turns them into short vertical videos with matching AI-generated audio, and stitches everything together in a Creatomate template. Once rendered, it uploads the final short to YouTube, updates the sheet’s status, and emails a notification—fully automating your faceless shorts production line.

## Technical Details

This workflow consists of 42 nodes that work together to automate your process. Here's what it uses:

- manualTrigger: When clicking ‘Test workflow’
- googleSheets: Grab Idea, Video Status, Update Sheet
- set: Set Animals, Set Prompts, Set Audio
- splitOut: Split Out
- @n8n/n8n-nodes-langchain.lmChatOpenAi: GPT 4o
- @n8n/n8n-nodes-langchain.agent: Image Prompt Agent, Sound Agent
- code: Remove \n, Split Out Parts (Kling), Split Out Parts
- httpRequest: Generate Image, Get Images, Generate Audio, Render Video, Download Video, Get Videos (Kling), Get Videos, Generate Videos (Kling), Generate Videos
- wait: 90 seconds, 8 Minutes, 25 Seconds, 2 minutes
- limit: Limit
- @n8n/n8n-nodes-langchain.lmChatGoogleGemini: Flash 2.0
- googleDrive: Upload to Drive, Share File
- merge: Merge
- youTube: Upload Video
- gmail: Notification
- scheduleTrigger: Schedule Trigger
- stickyNote: Sticky Note3, Sticky Note4, Sticky Note1, Sticky Note, Sticky Note2, Sticky Note5, Sticky Note6

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

