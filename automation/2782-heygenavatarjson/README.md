# HeyGen_Avatar.json

Categories: Content Creation

This n8n workflow automates the creation of AI avatar videos using HeyGen by extracting news from Morning Brew, summarizing it into a short video script, and generating a video with a selected avatar and voice. It includes polling logic to check video rendering status and supports dynamic scripting and customization using GPT via OpenRouter.

## Technical Details

This workflow consists of 19 nodes that work together to automate your process. Here's what it uses:

- manualTrigger: When clicking ‘Test workflow’
- httpRequest: Generate Video, Get Voices, Get Avatars, Get Video, News, Get Video1, Generate Video1
- stickyNote: Sticky Note, Sticky Note1, Sticky Note2, Sticky Note3, Sticky Note4, Sticky Note5
- @n8n/n8n-nodes-langchain.agent: Script Writer
- @n8n/n8n-nodes-langchain.lmChatOpenRouter: GPT 4.1 Mini
- wait: 30 Seconds, Wait
- if: If

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

