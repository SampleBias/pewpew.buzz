# Build Your Own Image Search Using AI Object Detection, CDN and ElasticSearchBuild Your Own Image Search Using AI Object Detection, CDN and ElasticSearch

Categories: Education, Social Media

Build Your Own Image Search Using AI Object Detection, CDN and ElasticSearchBuild Your Own Image Search Using AI Object Detection, CDN and ElasticSearch

## Technical Details

This workflow consists of 17 nodes that work together to automate your process. Here's what it uses:

- manualTrigger: When clicking "Test workflow"
- httpRequest: Fetch Source Image, Use Detr-Resnet-50 Object Classification, Upload to Cloudinary, Fetch Source Image Again
- splitOut: Split Out Results Only
- filter: Filter Score >= 0.9
- editImage: Crop Object From Image
- set: Set Variables
- elasticsearch: Create Docs In Elasticsearch
- stickyNote: Sticky Note, Sticky Note1, Sticky Note2, Sticky Note3, Sticky Note4, Sticky Note8, Sticky Note5

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

