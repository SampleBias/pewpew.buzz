# Deep_Research.json

Categories: Email, Content Creation

This workflow takes a user-submitted topic (and email), explodes it into five research subtopics, fetches web content with Tavily, then uses several Claude/OpenAI agents to draft styled HTML chapters, a table of contents, and a linked source list. All pieces are logged to a Google Sheet, assembled into a PDF via APITemplate.io, and the finished report is automatically emailed to the requester.

## Technical Details

This workflow consists of 93 nodes that work together to automate your process. Here's what it uses:

- formTrigger: On form submission
- @n8n/n8n-nodes-langchain.agent: Plan Topics, Intro, Writer, Writer1, Writer2, Writer3, Writer4, Sources, Table of Contents
- @n8n/n8n-nodes-langchain.lmChatOpenRouter: OpenRouter Chat Model, OpenRouter Chat Model1, OpenRouter Chat Model2, OpenRouter Chat Model3, OpenRouter Chat Model4, OpenRouter Chat Model5, OpenRouter Chat Model6, OpenRouter Chat Model7
- @n8n/n8n-nodes-langchain.outputParserStructured: 5 Topics, Title, Intro, Chapters
- splitOut: Split Out, Split Out1, Split Out2, Split Out3, Split Out4, Split Out5, Split Out6
- merge: Merge, Merge1, Merge3, Merge4, Merge5, Merge6, Merge7, Merge2
- set: Set Topics
- switch: Switch
- googleSheets: Google Sheets1, Google Sheets2, Google Sheets3, Google Sheets4, Google Sheets5, Get Sources, Send Sources, Get All Content, Send ToC, Send Intro, Get All Content1
- httpRequest: Tavily, Tavily1, Tavily2, Tavily3, Tavily4, Download PDF, Generate PDF
- code: Code, Code1, Code2, Code3, Code4, Combine Content, Combine, Combine1, Combine2, Combine3, Combine4
- aggregate: Aggregate, Aggregate1, Aggregate2, Aggregate3, Aggregate4, Aggregate5, Aggregate6, Aggregate7, Aggregate8, Aggregate9
- limit: Limit
- gmail: Send Report
- html: HTML, HTML1, HTML2, HTML3, HTML4
- stickyNote: Sticky Note, Sticky Note1, Sticky Note2, Sticky Note3, Sticky Note4, Sticky Note5, Sticky Note6, Sticky Note7, Sticky Note8, Sticky Note10

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

