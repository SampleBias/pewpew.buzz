#!/usr/bin/env python3
"""
Test script for workflow synchronization

This script tests the immediate synchronization of workflows
by checking if a specific workflow directory can be synced.
"""

import os
import sys
from dotenv import load_dotenv
from workflow_sync import get_workflow_from_filesystem, sync_workflow_to_database, get_supabase_client

def test_sync_workflow(workflow_dir=None):
    """Test syncing a specific workflow or the first available workflow"""
    # Load environment variables
    load_dotenv()
    
    # Get the supabase client
    supabase = get_supabase_client()
    
    # Get the base path for workflows
    base_path = os.path.join(os.path.dirname(__file__), 'automation')
    
    if not os.path.exists(base_path):
        print(f"Error: Automation directory '{base_path}' does not exist.")
        return False
    
    if workflow_dir:
        # Sync specific workflow
        workflow_path = os.path.join(base_path, workflow_dir)
        if not os.path.isdir(workflow_path):
            print(f"Error: Workflow directory '{workflow_dir}' does not exist.")
            return False
    else:
        # Find the first workflow directory
        try:
            workflow_dirs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
            if not workflow_dirs:
                print(f"Error: No workflow directories found in '{base_path}'.")
                return False
            workflow_dir = workflow_dirs[0]
        except Exception as e:
            print(f"Error listing workflow directories: {str(e)}")
            return False
    
    print(f"Testing synchronization for workflow '{workflow_dir}'...")
    
    # Get workflow data from filesystem
    workflow_data = get_workflow_from_filesystem(workflow_dir, base_path)
    
    if not workflow_data:
        print(f"Error: Invalid workflow directory or missing required files.")
        return False
    
    # Try to sync the workflow
    result = sync_workflow_to_database(workflow_data, supabase)
    
    if result:
        print(f"✅ SUCCESS: Workflow '{workflow_dir}' successfully synced to database!")
        return True
    else:
        print(f"❌ FAILURE: Could not sync workflow '{workflow_dir}' to database.")
        return False

if __name__ == "__main__":
    # Get workflow_dir from command line argument if provided
    workflow_dir = sys.argv[1] if len(sys.argv) > 1 else None
    
    if test_sync_workflow(workflow_dir):
        sys.exit(0)
    else:
        sys.exit(1) 