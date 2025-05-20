#!/usr/bin/env python3
"""
Test Supabase Connection

This script tests the connection to Supabase using both regular and service role keys.
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

print("=== Supabase Connection Test ===")
print(f"Supabase URL: {SUPABASE_URL[:20]}... (truncated for security)")

# Test with regular key
if SUPABASE_KEY:
    print("\n[Testing with regular key]")
    print(f"Key prefix: {SUPABASE_KEY[:5]}... (truncated for security)")
    
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        # Test a simple query
        response = supabase.table('workflow_ratings').select('id').limit(1).execute()
        print("✅ Regular key connection test: SUCCESS")
    except Exception as e:
        print(f"❌ Regular key connection test: FAILED")
        print(f"Error: {str(e)}")
else:
    print("\n❌ Regular key not found in environment variables")

# Test with service role key
if SUPABASE_SECRET_KEY:
    print("\n[Testing with service role key]")
    print(f"Key prefix: {SUPABASE_SECRET_KEY[:5]}... (truncated for security)")
    
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_SECRET_KEY)
        # Test a simple query
        response = supabase.table('workflow_ratings').select('id').limit(1).execute()
        print("✅ Service role key connection test: SUCCESS")
        
        # Test a more privileged operation if possible
        try:
            # Try to execute a raw query (this requires service role permissions)
            query = "SELECT COUNT(*) FROM workflow_ratings"
            response = supabase.rpc('pgmeta_query', {'query': query}).execute()
            print("✅ Service role privileges test: SUCCESS")
        except Exception as e:
            print(f"❓ Service role privileges test: INCONCLUSIVE")
            print(f"This could be because the pgmeta_query function doesn't exist or due to other reasons")
            print(f"Error: {str(e)}")
    except Exception as e:
        print(f"❌ Service role key connection test: FAILED")
        print(f"Error: {str(e)}")
else:
    print("\n❌ Service role key not found in environment variables")

print("\n=== Connection Test Complete ===")

# Final advice
print("\nRecommendations:")
if not SUPABASE_KEY and not SUPABASE_SECRET_KEY:
    print("- Add either SUPABASE_KEY or SUPABASE_SECRET_KEY (or both) to your .env file")
    sys.exit(1)
elif SUPABASE_SECRET_KEY and not SUPABASE_KEY:
    print("- You're using only the service role key, which is fine for development")
    print("- Consider adding a regular SUPABASE_KEY for public endpoints")
elif SUPABASE_KEY and not SUPABASE_SECRET_KEY:
    print("- You're using only the regular key")
    print("- Consider adding SUPABASE_SECRET_KEY to enable privileged operations")
else:
    print("- You have both keys configured, which provides the most flexibility")

# Exit with appropriate code
if (SUPABASE_KEY and not SUPABASE_SECRET_KEY) or (SUPABASE_SECRET_KEY and not SUPABASE_KEY) or (SUPABASE_KEY and SUPABASE_SECRET_KEY):
    sys.exit(0)
else:
    sys.exit(1) 