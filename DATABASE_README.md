# PewPew.buzz Database Structure

This document explains the database structure used in PewPew.buzz for managing users, workflows, and analytics.

## Overview

PewPew.buzz uses Supabase as its database backend. The database is structured around several key entities:

1. **User Management** - Tracking user accounts, profiles, and preferences
2. **Workflow Management** - Storing n8n workflows, their metadata, categories, and ratings
3. **Analytics** - Tracking views, downloads, and other user interactions

## Schema Setup

To set up the schema in your Supabase instance:

1. Log in to your Supabase dashboard
2. Go to the SQL Editor
3. Run the SQL script from `supabase_schema.sql`

## Table Descriptions

### User Management

#### `user_profiles`
Stores additional user information beyond Supabase Auth.
- `id`: UUID (linked to auth.users)
- `display_name`: User's displayed name
- `website`: User's website
- `avatar_url`: URL to user's avatar
- `bio`: User's biography

#### `user_preferences`
Stores user preferences for the website.
- `user_id`: UUID (linked to auth.users)
- `theme`: User's theme preference
- `email_notifications`: Whether user wants email notifications

### Workflow Management

#### `workflows`
The main table for storing automation workflows.
- `id`: Serial ID
- `slug`: Text identifier for the workflow (usually a formatted version of the title or folder name)
- `title`: Workflow title
- `description`: Short description of what the workflow does
- `author_id`: UUID of the author (if they have an account)
- `author_name`: Text name of the author (preserved even if account is deleted)
- `json_content`: JSONB containing the actual n8n workflow
- `readme_content`: Markdown content explaining the workflow
- `created_at`, `updated_at`: Timestamps
- `published`: Whether the workflow is publicly visible
- `published_date`: When the workflow was published
- `views`, `downloads`: Counter fields
- Flags for workflow type: `is_generated`, `is_submitted`, `is_extracted`

#### `workflow_categories`
Associates workflows with multiple categories.
- `workflow_id`: Reference to workflows.id
- `category`: Category name

#### `workflow_ratings`
Stores the count of upvotes and downvotes for each workflow.
- `workflow_id`: Text identifier for the workflow
- `upvotes`, `downvotes`: Count of votes

#### `user_ratings`
Tracks which users have rated which workflows.
- `user_id`: UUID of the user
- `workflow_id`: ID of the workflow
- `rating_type`: 'upvote' or 'downvote'

### Analytics

#### `workflow_views`
Tracks when users view workflow details.
- `workflow_id`: ID of the viewed workflow
- `user_id`: UUID of the user (if logged in)
- `viewed_at`: Timestamp
- `ip_address`, `user_agent`: For anonymous tracking

#### `workflow_downloads`
Tracks when users download workflows.
- `workflow_id`: ID of the downloaded workflow
- `user_id`: UUID of the user (if logged in)
- `downloaded_at`: Timestamp
- `ip_address`, `user_agent`: For anonymous tracking

## Row Level Security (RLS)

All tables have Row Level Security enabled to ensure data is only accessible to users with appropriate permissions:

- Public workflows are visible to everyone
- Private workflows are only visible to their authors
- Users can only modify their own data
- Ratings are publicly viewable but only modifiable by the rating user

## Database Functions

### `rate_workflow(workflow_id, user_id, rating_type)`

A secure database function for handling workflow ratings that:
- Prevents duplicate ratings from the same user
- Updates the counts in workflow_ratings
- Records individual user ratings

## Migrating from File-based Storage

To migrate existing workflows from the file-based system to the database:

1. Run the provided migration script:
   ```
   python migrate_to_database.py
   ```

2. This script will:
   - Read all workflows from the `automation` directory
   - Extract metadata from README files and meta.json files
   - Create corresponding records in the database
   - Set up initial ratings

3. After migration, you can adapt the application to use the database instead of the file system.

## Transitioning the Application

To modify the application to use the database:

1. Replace file system reads with database queries
2. Update API endpoints to work with the database
3. Add authentication checks using Supabase Auth

## Benefits of Using the Database

- **Better Performance**: Faster querying and filtering
- **More Features**: User management, ratings, analytics
- **Scalability**: Handles growing amounts of workflows and users
- **Security**: Row Level Security and proper authentication
- **Analytics**: Track popularity and usage patterns 