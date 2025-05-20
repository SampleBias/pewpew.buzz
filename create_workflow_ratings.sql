-- Create the workflow_ratings table if it doesn't exist
CREATE TABLE IF NOT EXISTS workflow_ratings (
    id SERIAL PRIMARY KEY,
    workflow_id TEXT NOT NULL UNIQUE, -- Using the folder ID for compatibility
    upvotes INTEGER DEFAULT 0,
    downvotes INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Enable RLS on the table
ALTER TABLE workflow_ratings ENABLE ROW LEVEL SECURITY;

-- Create a policy to allow public access to view ratings
-- First drop the policy if it exists to avoid errors
DROP POLICY IF EXISTS "Anyone can view workflow ratings" ON workflow_ratings;

CREATE POLICY "Anyone can view workflow ratings"
ON workflow_ratings FOR SELECT
TO authenticated, anon
USING (true);

-- Create a trigger to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = CURRENT_TIMESTAMP;
   RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Add the trigger to the table
DROP TRIGGER IF EXISTS update_workflow_ratings_timestamp ON workflow_ratings;
CREATE TRIGGER update_workflow_ratings_timestamp
BEFORE UPDATE ON workflow_ratings
FOR EACH ROW EXECUTE PROCEDURE update_timestamp(); 