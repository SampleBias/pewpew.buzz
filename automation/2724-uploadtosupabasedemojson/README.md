# Upload_to_Supabase_Demo.json

Categories: Data Management

The Upload to Supabase Demo workflow automatically ingests newly added or updated files from a specified Google Drive folder, extracts their text, converts it into vector embeddings using OpenAI, and uploads the data into a Supabase vector store for future retrieval. It ensures documents are updated cleanly by deleting outdated versions before re-indexing the latest content.

## Technical Details

This workflow consists of 18 nodes that work together to automate your process. Here's what it uses:

- set: Set ID, Set ID 2
- extractFromFile: Extract from File, Extract from File1
- @n8n/n8n-nodes-langchain.vectorStoreSupabase: Supabase Vector Store, Supabase Vector Store1
- @n8n/n8n-nodes-langchain.documentDefaultDataLoader: Default Data Loader, Default Data Loader1
- @n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter: Recursive Character Text Splitter, Recursive Character Text Splitter1
- @n8n/n8n-nodes-langchain.embeddingsOpenAi: Embeddings OpenAI, Embeddings OpenAI1
- googleDriveTrigger: File Updated, New File
- googleDrive: Downloading File, Download File 2
- supabase: Delete Row(s)
- limit: Keep First ID

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

