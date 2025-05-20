-- Add missing RLS policies for workflow_ratings table

-- First check if the workflow_ratings table exists
DO $$
BEGIN
    IF EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name = 'workflow_ratings'
    ) THEN
        -- Drop existing policies that might conflict
        DROP POLICY IF EXISTS "Anyone can insert workflow ratings" ON workflow_ratings;
        DROP POLICY IF EXISTS "Anyone can update workflow ratings" ON workflow_ratings;
        
        -- Create policy for inserting new ratings
        CREATE POLICY "Anyone can insert workflow ratings" 
        ON workflow_ratings FOR INSERT
        TO authenticated, anon
        WITH CHECK (true);
        
        -- Create policy for updating existing ratings
        CREATE POLICY "Anyone can update workflow ratings" 
        ON workflow_ratings FOR UPDATE
        TO authenticated, anon
        USING (true);
        
        RAISE NOTICE 'Successfully added RLS policies for workflow_ratings table';
    ELSE
        RAISE NOTICE 'workflow_ratings table does not exist';
    END IF;
END
$$; 