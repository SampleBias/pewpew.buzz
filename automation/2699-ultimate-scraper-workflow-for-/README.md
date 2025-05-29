# Ultimate Scraper Workflow for n8n

Categories: AI, Analytics, Data Management

Ultimate Scraper Workflow for n8n

## Technical Details

This workflow consists of 63 nodes that work together to automate your process. Here's what it uses:

- html: Extract First Url Match
- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model, OpenAI Chat Model1, OpenAI Chat Model2
- httpRequest: Clean Webdriver , Delete Session, Delete Session2, Delete Session3, Delete Session1, Delete Session4, Delete Session5, Inject Cookie, Go on url, Delete Session6, Google search Query , Create Selenium Session, Get ScreenShot 1, Refresh browser, Get ScreenShot , Delete Session7, Get ScreenShot 2, Go on ip-api.com, Delete Session8, Resize browser window, Go on url1, Go on url2, Go on url3
- if: If Block1, If, Check if empty of NA, If Block, If Target Url, If1, If2, If3
- limit: Limit
- respondToWebhook: Success with cookie, Respond to Webhook2, Error, Error1, Error2, Respond to Webhook3, Success, Error3, Error can't find url
- code: Code
- @n8n/n8n-nodes-langchain.informationExtractor: Information Extractor, Information Extractor1, Information Extractor2
- convertToFile: Convert to File, Convert to File1, Convert to File2
- stickyNote: Sticky Note, Sticky Note1, Sticky Note2, Sticky Note3, Sticky Note4, Sticky Note5, Sticky Note6
- set: Edit Fields (For testing prupose )
- @n8n/n8n-nodes-langchain.openAi: OpenAI, OpenAI1
- webhook: Webhook

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

