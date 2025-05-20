#!/usr/bin/env python3
"""
Script to check if the required tables exist in Supabase.
"""

import os
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# List of tables to check
TABLES = [
    'user_profiles',
    'user_preferences',
    'workflows',
    'workflow_categories',
    'workflow_ratings',
    'user_ratings',
    'workflow_views',
    'workflow_downloads'
]

def check_table_exists(table_name):
    """Check if a table exists by attempting to query it"""
    try:
        # Try to select a single row from the table
        result = supabase.table(table_name).select('*').limit(1).execute()
        print(f"✅ Table '{table_name}' exists")
        return True
    except Exception as e:
        print(f"❌ Table '{table_name}' does not exist or cannot be accessed: {str(e)}")
        return False

def main():
    """Main function to check all tables"""
    print("Checking Supabase tables...")
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Error: SUPABASE_URL or SUPABASE_KEY not found in environment variables")
        return
    
    existing_tables = []
    missing_tables = []
    
    for table in TABLES:
        if check_table_exists(table):
            existing_tables.append(table)
        else:
            missing_tables.append(table)
    
    print("\nSummary:")
    print(f"- {len(existing_tables)} tables exist: {', '.join(existing_tables) if existing_tables else 'None'}")
    print(f"- {len(missing_tables)} tables are missing: {', '.join(missing_tables) if missing_tables else 'None'}")
    
    if missing_tables:
        print("\nTo create the missing tables, run the SQL script in the Supabase SQL Editor:")
        print("1. Log into your Supabase dashboard")
        print("2. Go to SQL Editor")
        print("3. Copy the contents of 'supabase_schema.sql'")
        print("4. Run the SQL script")

if __name__ == "__main__":
    main() 