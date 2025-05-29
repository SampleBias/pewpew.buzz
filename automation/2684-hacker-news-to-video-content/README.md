# Hacker News to Video Content

Categories: AI, Content Creation, Ecommerce

Hacker News to Video Content

## Technical Details

This workflow consists of 48 nodes that work together to automate your process. Here's what it uses:

- manualTrigger: When clicking ‘Test workflow’
- hackerNews: Hacker News
- splitInBatches: Loop Over Items
- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model3
- @n8n/n8n-nodes-langchain.toolHttpRequest: HTTP Request1
- @n8n/n8n-nodes-langchain.outputParserStructured: Structured Output Parser
- s3: Upload to Minio
- set: News1, Prompt Settings1
- httpRequest: Leo - Improve Prompt, Leo - Get imageId, Runway - Create Video, Runway - Get Video, Get Image, Leo - Generate Image, Instagram, Leo - Improve Prompt2, Leo - Generate Image2, Leo - Get imageId2, Runway - Create Video2, Runway - Get Video2, Cre - Generate Video1, Cre - Get Video
- wait: Wait2, Wait1, Wait3, Wait4, Wait6
- stickyNote: Sticky Note, Sticky Note1, Sticky Note2, Sticky Note3, Sticky Note4, Sticky Note6, Sticky Note7, Sticky Note5, Sticky Note8
- if: If Topic
- limit: Limit
- @n8n/n8n-nodes-langchain.openAi: Image Analysis, Article Prep
- @n8n/n8n-nodes-langchain.agent: Article Analysis
- dropbox: Dropbox
- googleDrive: Google Drive
- microsoftOneDrive: Microsoft OneDrive
- youTube: YouTube
- twitter: X
- linkedIn: LinkedIn

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

