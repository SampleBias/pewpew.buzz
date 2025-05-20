#!/usr/bin/env python3
"""
Check SQL Installation

This script checks if the required SQL files have been properly executed in Supabase.
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
    
    print("\n=== Checking SQL Installation ===")
    
    # Check if required tables exist
    required_tables = [
        'workflow_ratings',
        'workflows',
        'workflow_categories',
        'workflow_sync_log'
    ]
    
    missing_tables = []
    for table in required_tables:
        try:
            response = supabase.table(table).select('*').limit(1).execute()
            print(f"✅ Table '{table}' exists")
        except Exception as e:
            print(f"❌ Table '{table}' doesn't exist or is not accessible: {str(e)}")
            missing_tables.append(table)
    
    # Check if required functions exist
    required_functions = [
        'sync_workflow_to_database',
        'mark_workflow_deleted',
        'update_timestamp'
    ]
    
    missing_functions = []
    for function in required_functions:
        try:
            # Check if the function exists in Supabase
            query = f"""
            SELECT proname 
            FROM pg_proc 
            WHERE proname = '{function}'
            """
            response = supabase.rpc('pgmeta_query', {'query': query}).execute()
            
            if response.data and len(response.data) > 0:
                print(f"✅ Function '{function}' exists")
            else:
                print(f"❌ Function '{function}' doesn't exist")
                missing_functions.append(function)
        except Exception as e:
            print(f"❌ Error checking function '{function}': {str(e)}")
            missing_functions.append(function)
    
    # Check if required policies exist
    required_policies = [
        "Anyone can view workflow ratings",
        "Anyone can insert workflow ratings",
        "Anyone can update workflow ratings"
    ]
    
    missing_policies = []
    try:
        query = """
        SELECT policyname 
        FROM pg_policies
        WHERE tablename = 'workflow_ratings'
        """
        response = supabase.rpc('pgmeta_query', {'query': query}).execute()
        
        if response.data:
            existing_policies = [policy['policyname'] for policy in response.data]
            print(f"Found policies on workflow_ratings: {', '.join(existing_policies)}")
            
            for policy in required_policies:
                if policy in existing_policies:
                    print(f"✅ Policy '{policy}' exists")
                else:
                    print(f"❌ Policy '{policy}' doesn't exist")
                    missing_policies.append(policy)
        else:
            print("❌ No policies found on workflow_ratings table")
            missing_policies = required_policies
    except Exception as e:
        print(f"❌ Error checking policies: {str(e)}")
        missing_policies = required_policies
    
    # Final verdict
    print("\n=== Installation Status ===")
    
    if missing_tables:
        print(f"❌ {len(missing_tables)} missing tables: {', '.join(missing_tables)}")
        print("   You need to execute supabase_schema_fixed.sql")
    else:
        print("✅ All required tables exist")
    
    if missing_functions:
        print(f"❌ {len(missing_functions)} missing functions: {', '.join(missing_functions)}")
        print("   You need to execute workflow_synchronization.sql")
    else:
        print("✅ All required functions exist")
    
    if missing_policies:
        print(f"❌ {len(missing_policies)} missing policies: {', '.join(missing_policies)}")
        print("   You need to execute add_workflow_ratings_policy.sql")
    else:
        print("✅ All required policies exist")
    
    if missing_tables or missing_functions or missing_policies:
        print("\n⚠️ Your SQL installation is incomplete. Follow these steps:")
        if missing_tables:
            print("1. Execute supabase_schema_fixed.sql in the Supabase SQL Editor")
        if missing_functions:
            print("2. Execute workflow_synchronization.sql in the Supabase SQL Editor")
        if missing_policies:
            print("3. Execute add_workflow_ratings_policy.sql in the Supabase SQL Editor")
    else:
        print("\n✅ Your SQL installation is complete!")
    
except Exception as e:
    print(f"Error connecting to Supabase: {str(e)}")
    sys.exit(1)

print("\n=== Check Complete ===") 