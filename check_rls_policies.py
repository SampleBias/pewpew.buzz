#!/usr/bin/env python3
"""
Check RLS Policies

This script checks the RLS policies for workflow-related tables in Supabase.
"""

import os
import sys
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()

# Get Supabase credentials
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
SUPABASE_SECRET_KEY = os.environ.get('SUPABASE_SECRET_KEY')

# Use the service role key if available
supabase_key = SUPABASE_SECRET_KEY if SUPABASE_SECRET_KEY else SUPABASE_KEY

if not SUPABASE_URL or not supabase_key:
    print("Error: SUPABASE_URL and either SUPABASE_KEY or SUPABASE_SECRET_KEY must be set")
    sys.exit(1)

try:
    # Create the Supabase client
    supabase = create_client(SUPABASE_URL, supabase_key)
    
    # List of tables to check
    tables = [
        'workflows',
        'workflow_categories',
        'workflow_ratings',
        'workflow_sync_log',
        'user_ratings'
    ]
    
    print("\n=== Checking Table Access and RLS Policies ===")
    
    # Check if tables exist and try to access them
    for table in tables:
        print(f"\nChecking table: {table}")
        try:
            # Try to select one row
            response = supabase.table(table).select('*').limit(1).execute()
            print(f"✅ Table '{table}' exists and is accessible")
            print(f"  Records returned: {len(response.data)}")
            
            # Try to get RLS policies using metadata function (service role only)
            if SUPABASE_SECRET_KEY:
                try:
                    # This requires service role permissions
                    query = f"""
                    SELECT policyname, cmd, permissive, roles, qual
                    FROM pg_policies
                    WHERE tablename = '{table}'
                    """
                    policy_response = supabase.rpc('pgmeta_query', {'query': query}).execute()
                    
                    if policy_response.data and len(policy_response.data) > 0:
                        print(f"  RLS Policies for '{table}':")
                        for policy in policy_response.data:
                            print(f"    - {policy['policyname']} ({policy['cmd']}): {policy['roles']}")
                    else:
                        print(f"  No RLS policies found for '{table}'")
                except Exception as e:
                    print(f"  Could not retrieve RLS policies: {str(e)}")
        except Exception as e:
            print(f"❌ Error accessing table '{table}': {str(e)}")
            
    # Try to execute the special sync function
    print("\nChecking function: sync_workflow_to_database")
    try:
        # Just checking if the function exists
        dummy_data = {
            'p_slug': 'test_slug',
            'p_title': 'Test Title',
            'p_description': 'Test Description',
            'p_author_name': 'Test Author',
            'p_json_content': {"test": "data"},
            'p_readme_content': "Test readme",
            'p_categories': ["Test"],
            'p_is_generated': False,
            'p_is_submitted': False,
            'p_is_extracted': False
        }
        
        # Don't actually execute, just check if it exists
        # result = supabase.rpc('sync_workflow_to_database', dummy_data).execute()
        # Just check if the function exists in Supabase
        query = """
        SELECT proname 
        FROM pg_proc 
        WHERE proname = 'sync_workflow_to_database'
        """
        func_response = supabase.rpc('pgmeta_query', {'query': query}).execute()
        
        if func_response.data and len(func_response.data) > 0:
            print("✅ Function 'sync_workflow_to_database' exists")
        else:
            print("❌ Function 'sync_workflow_to_database' does not exist")
    except Exception as e:
        print(f"❌ Error checking function 'sync_workflow_to_database': {str(e)}")
    
except Exception as e:
    print(f"Error connecting to Supabase: {str(e)}")
    sys.exit(1)

print("\n=== RLS Policy Check Complete ===") 