# OpenAI_Image_Gen_LinkedIn_Post.json

Categories: Content Creation

This workflow turns a user-submitted topic and target audience into a polished LinkedIn package: it researches the topic in real time with Tavily, drafts a professional post via GPT-4.1, then has a second agent craft an on-brand image prompt, generates the graphic with OpenAI’s image API, and finally emails (or optionally posts) the finished post plus image. Behind the scenes it stitches together form capture, web search, multi-step prompt engineering, image generation, binary conversion, and distribution through Gmail or LinkedIn—all automatically in one run.

## Technical Details

This workflow consists of 20 nodes that work together to automate your process. Here's what it uses:

- @n8n/n8n-nodes-langchain.toolHttpRequest: Tavily
- @n8n/n8n-nodes-langchain.lmChatOpenRouter: GPT_4.1
- linkedIn: LinkedIn
- @n8n/n8n-nodes-langchain.agent: LinkedIn Post Agent, Image Prompt Agent
- httpRequest: Generate Image, Generate Image1
- convertToFile: Convert to Binary, Convert to File
- gmail: Send Post
- formTrigger: On form submission
- stickyNote: Sticky Note, Sticky Note1, Sticky Note3, Sticky Note4, Sticky Note5, Sticky Note2, Sticky Note6, Sticky Note7
- manualTrigger: When clicking ‘Test workflow’

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

