# Mistral_OCR.json

Categories: Data Management, Content Creation

This workflow lets someone upload a document through a web form, sends the file to Mistral’s OCR service, and retrieves AI-extracted text (plus an image preview) via the API. Behind the scenes it uploads the file, grabs a 24-hour signed URL, calls mistral-ocr-latest, and leaves the parsed results ready for downstream use.

## Technical Details

This workflow consists of 6 nodes that work together to automate your process. Here's what it uses:

- formTrigger: On form submission
- httpRequest: Upload to Mistral, Get Signed URL, Get OCR Results
- stickyNote: Sticky Note, Sticky Note1

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

