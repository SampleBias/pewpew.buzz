# Workflow Rating System Setup

This document explains how to set up the thumbs up/down rating system for automation workflows in pewpew.buzz.

## Database Setup

1. Log into your Supabase account
2. Navigate to the SQL Editor
3. Run the following SQL query to create the necessary table:

```sql
CREATE TABLE IF NOT EXISTS workflow_ratings (
  id SERIAL PRIMARY KEY,
  workflow_id VARCHAR(255) NOT NULL UNIQUE,
  upvotes INTEGER DEFAULT 0,
  downvotes INTEGER DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

4. Create a Row Level Security (RLS) policy to control access:

```sql
-- Enable RLS on the workflow_ratings table
ALTER TABLE workflow_ratings ENABLE ROW LEVEL SECURITY;

-- Create a policy that allows anyone to read ratings
CREATE POLICY "Anyone can read ratings" 
ON workflow_ratings FOR SELECT 
USING (true);

-- Create a policy that allows authenticated users to create and update ratings
CREATE POLICY "Authenticated users can create and update ratings" 
ON workflow_ratings FOR ALL 
USING (auth.role() = 'authenticated');
```

## Features

The rating system provides:

1. Thumbs up/down buttons on each automation card
2. Visual count of upvotes and downvotes
3. Animation effect when rating is submitted
4. Real-time update of rating counts

## How It Works

1. When a user clicks the thumbs up or thumbs down button:
   - A POST request is sent to `/api/workflow/rating/<workflow_id>`
   - The server updates the rating in the Supabase database
   - The updated counts are returned and displayed on the card

2. When loading the dashboard, all workflow ratings are fetched at once for efficiency.

## API Endpoints

- `GET /api/workflow/rating/<workflow_id>`: Get the current rating for a workflow
- `POST /api/workflow/rating/<workflow_id>`: Submit a rating (upvote or downvote)

## Customization

You can customize the appearance of the rating system by modifying the CSS in the `dashboard.html` template. 