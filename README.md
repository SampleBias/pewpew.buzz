# PewPew.buzz

PewPew.buzz is a platform for creating and sharing n8n automation workflows. 

## Features

- Browse a gallery of pre-built automation workflows
- Generate new workflows using AI
- Extract workflows from screenshots 
- Add your own workflows to the gallery
- Rate and download workflows
- Database storage for workflows with file system sync

## Setup

1. Clone this repository
2. Install requirements: `pip install -r requirements.txt`
3. Set up environment variables:
   - Create a `.env` file with the following variables:
     - `FLASK_SECRET_KEY` - Secret key for Flask session
     - `AUTH0_CLIENT_ID` - Auth0 client ID (for login)
     - `AUTH0_CLIENT_SECRET` - Auth0 client secret
     - `AUTH0_DOMAIN` - Auth0 domain
     - `AUTH0_CALLBACK_URL` - Auth0 callback URL
     - `GEMINI_API_KEY` - Google Gemini API key (for AI features)
     - `SUPABASE_URL` - Supabase project URL
     - `SUPABASE_KEY` - Supabase API key

4. Set up the database:
   ```
   ./setup_workflow_database.sh
   ```
   This script will:
   - Create necessary database tables in Supabase
   - Set up workflow synchronization functions
   - Migrate existing workflows to the database
   - Configure automatic synchronization

5. Run the application:
   ```
   python app.py
   ```

## Directory Structure

- `app.py` - Main Flask application
- `workflow_builder.py` - n8n workflow builder and AI generation
- `workflow_sync.py` - Database synchronization utilities
- `templates/` - HTML templates
- `static/` - CSS, JavaScript, and image files
- `automation/` - Workflow files (JSON and README)

## Database System

The application uses Supabase as its database backend, with tables for:

- Workflows (json_content, metadata)
- Workflow categories
- Ratings and user interactions

Workflows are stored in both the filesystem and database, with automatic synchronization. See `WORKFLOW_DATABASE_SYNC.md` for details.

## API Endpoints

- `/api/generate-workflow` - Generate a workflow with AI
- `/api/extract-workflow-from-image` - Extract workflow from screenshot
- `/api/add-workflow` - Add a user-submitted workflow
- `/api/workflow/rating/:id` - Get or update workflow ratings

## License

MIT
