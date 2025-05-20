#!/usr/bin/env python3
"""
Apply RLS Policies Script

This script applies the necessary RLS policies to the workflow_ratings table in Supabase.
"""

import os
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Error: SUPABASE_URL and SUPABASE_KEY must be set in your .env file")
    exit(1)

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# SQL to apply the policies
policies_sql = """
-- Add missing RLS policies for workflow_ratings table
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
"""

try:
    # Execute raw SQL using Supabase API
    print("Applying RLS policies to workflow_ratings table...")
    # Note: This specific API call might vary based on the Supabase Python client implementation
    # Some versions of the client might require different approaches to run raw SQL
    response = supabase.rpc('pgmeta_query', {'query': policies_sql}).execute()
    
    print("Successfully applied RLS policies!")
    print("You should now be able to add and update workflow ratings.")
except Exception as e:
    print(f"Error applying policies: {str(e)}")
    print("You may need to apply the policies manually using the Supabase SQL Editor:")
    print("\n" + policies_sql) 