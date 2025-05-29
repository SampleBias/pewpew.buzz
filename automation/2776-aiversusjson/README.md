# AI_Versus.json

Categories: Content Creation

This flow picks a “main character” animal from Google Sheets, has GPT name eight opponents, then uses PIAPI to generate close-ups and victory scenes, records the image URLs back to the sheet, and finally stitches everything into a vertical eight-round fight video with Creatomate. Once the render is ready, it updates the sheet, uploads the finished short to Blotato, and auto-publishes it to Instagram, TikTok, and YouTube.

## Technical Details

This workflow consists of 43 nodes that work together to automate your process. Here's what it uses:

- httpRequest: Render Video, Get Video, Generate Close Ups, Get Close Ups, Generate Scene, Get Winners, Upload to Blotato, Instagram, TikTok, YouTube
- googleSheets: Get Main Character, Add Close Ups, Add Winner, Get Elements, Google Sheets
- @n8n/n8n-nodes-langchain.agent: Scene Creator, Image Prompt Generator, Winner Image Prompt
- @n8n/n8n-nodes-langchain.lmChatOpenRouter: GPT 4.1-mini, GPT 4.1
- splitOut: Split Out, Split Out1
- set: Main Character, Opponents
- merge: Merge, Merge1
- @n8n/n8n-nodes-langchain.outputParserStructured: Scenes, Close Ups
- wait: 90 seconds, 90_seconds, 90_Seconds
- aggregate: Aggregate, Aggregate1
- stickyNote: Sticky Note, Sticky Note1, Sticky Note2, Sticky Note3, Sticky Note4, Sticky Note5, Sticky Note6, Sticky Note7, Sticky Note8
- scheduleTrigger: Schedule Trigger

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

