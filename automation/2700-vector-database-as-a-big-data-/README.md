# Vector Database as a Big Data Analysis Tool for AI Agents [1_3 anomaly][1_2 KNN]

Categories: AI, Analytics, Data Management

Vector Database as a Big Data Analysis Tool for AI Agents [1_3 anomaly][1_2 KNN]

## Technical Details

This workflow consists of 25 nodes that work together to automate your process. Here's what it uses:

- manualTrigger: When clicking ‘Test workflow’
- googleCloudStorage: Google Cloud Storage
- set: Get fields for Qdrant, Qdrant cluster variables, Batches in the API's format
- httpRequest: Embed crop image, Create Qdrant Collection, Check Qdrant Collection Existence, Batch Upload to Qdrant, Payload index on crop_name
- code: Split in batches, generate uuids for Qdrant points
- if: If collection exists
- stickyNote: Sticky Note, Sticky Note1, Sticky Note2, Sticky Note3, Sticky Note4, Sticky Note5, Sticky Note6, Sticky Note7, Sticky Note9, Sticky Note11, Sticky Note8, Sticky Note10
- filter: Filtering out tomato to test anomalies

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

