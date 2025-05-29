# Product_Videos.json

Categories: Email

Users upload a product photo, title, description and email; the workflow refines the image with an AI-generated prompt, uploads it, and produces a polished marketing shot plus a 10-second rotating video via Runway. Once the video is finished it emails the user a link to the enhanced photo and the freshly generated product-spin video.

## Technical Details

This workflow consists of 24 nodes that work together to automate your process. Here's what it uses:

- formTrigger: On form submission
- stickyNote: Sticky Note, Sticky Note1, Sticky Note2, Sticky Note3, Sticky Note4, Sticky Note5, Sticky Note6, Sticky Note7, Sticky Note8, Sticky Note9
- googleDrive: Upload Photo, Download File
- @n8n/n8n-nodes-langchain.lmChatOpenRouter: GPT 4.1
- httpRequest: Create Image, Get URL, Generate Video, Get Video
- convertToFile: Convert to File
- if: If
- wait: 5 Secs, 60 Seconds
- gmail: Send Finished Products
- @n8n/n8n-nodes-langchain.agent: Product Photography Agent

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

