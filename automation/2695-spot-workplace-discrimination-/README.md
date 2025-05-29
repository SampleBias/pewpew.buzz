# Spot Workplace Discrimination Patterns with AI

Categories: AI, HR

Spot Workplace Discrimination Patterns with AI

## Technical Details

This workflow consists of 38 nodes that work together to automate your process. Here's what it uses:

- manualTrigger: When clicking ‘Test workflow’
- @n8n/n8n-nodes-langchain.lmChatOpenAi: OpenAI Chat Model1, OpenAI Chat Model2, OpenAI Chat Model
- merge: Merge
- set: SET company_name, Define dictionary of demographic keys, Define contributions to variance, Set variance and std_dev, Sort Effect Sizes, Calculate Z-Scores and Effect Sizes, Specify additional parameters for scatterplot
- httpRequest: ScrapingBee Search Glassdoor, ScrapingBee GET company page contents, ScrapingBee GET Glassdoor Reviews Content, Quickchart Scatterplot
- html: Extract company url path, Extract reviews page url path, Extract Overall Review Summary, Extract Demographics Module
- @n8n/n8n-nodes-langchain.informationExtractor: Extract overall ratings and distribution percentages, Extract demographic distributions
- code: Calculate P-Scores, Format dataset for scatterplot
- quickChart: QuickChart Bar Chart
- stickyNote: Sticky Note, Sticky Note1, Sticky Note2, Sticky Note3, Sticky Note4, Sticky Note6, Sticky Note7, Sticky Note8, Sticky Note9, Sticky Note10, Sticky Note11, Sticky Note12
- @n8n/n8n-nodes-langchain.chainLlm: Text Analysis of Bias Data

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

