#!/usr/bin/env python3
"""
Workflow Synchronization Script

This script manages the synchronization between file-based workflows and the database.
It can be run as a one-time migration or as a scheduled task to keep
file-based workflows and the database in sync.
"""

import os
import json
import re
import datetime
import argparse
import sys
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

# Initialize Supabase client
def get_supabase_client():
    """Get a configured Supabase client"""
    if not SUPABASE_URL:
        print("Error: SUPABASE_URL must be set in .env file")
        sys.exit(1)
    
    # First try to use the service role key if available
    service_key = os.environ.get('SUPABASE_SECRET_KEY')
    if service_key:
        print("Using service role key for Supabase connection")
        return create_client(SUPABASE_URL, service_key)
        
    # Fall back to regular key
    regular_key = os.environ.get('SUPABASE_KEY')
    if not regular_key:
        print("Error: Neither SUPABASE_KEY nor SUPABASE_SECRET_KEY is set in .env file")
        sys.exit(1)
        
    print("Using regular key for Supabase connection")
    return create_client(SUPABASE_URL, regular_key)

# Functions for reading workflow information from files
def read_markdown_value(content, key):
    """Extract a value from markdown content by key"""
    pattern = rf"{key}:\s*(.*?)(?:\n|$)"
    match = re.search(pattern, content, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None

def extract_categories(content):
    """Extract categories from markdown content"""
    categories_text = read_markdown_value(content, "Categories")
    if categories_text:
        return [cat.strip() for cat in categories_text.split(',')]
    return ["Uncategorized"]

def extract_first_paragraph(content):
    """Extract the first paragraph from markdown content (skipping the title)"""
    lines = content.strip().split('\n')
    
    # Skip the title line
    start_idx = 1
    
    # Skip any category lines or empty lines
    while start_idx < len(lines) and (not lines[start_idx].strip() or lines[start_idx].lower().startswith('categories:')):
        start_idx += 1
    
    # Find the end of the paragraph
    end_idx = start_idx
    while end_idx < len(lines) and lines[end_idx].strip() and not lines[end_idx].startswith('#'):
        end_idx += 1
    
    if start_idx < len(lines):
        return ' '.join(lines[start_idx:end_idx]).strip()
    
    return "No description available."

def get_workflow_from_filesystem(workflow_dir, base_path):
    """Get workflow data from file system"""
    dir_path = os.path.join(base_path, workflow_dir)
    
    # Required files
    workflow_file = os.path.join(dir_path, 'workflow.json')
    readme_file = os.path.join(dir_path, 'README.md')
    meta_file = os.path.join(dir_path, 'meta.json')
    
    if not os.path.exists(workflow_file) or not os.path.exists(readme_file):
        return None
    
    # Load workflow JSON
    with open(workflow_file, 'r', encoding='utf-8') as f:
        workflow_json = json.load(f)
    
    # Load README content
    with open(readme_file, 'r', encoding='utf-8') as f:
        readme_content = f.read()
    
    # Extract workflow title from README (first line after removing the # prefix)
    title_match = re.search(r'^#\s*(.*?)$', readme_content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else workflow_dir
    
    # Extract description
    description = extract_first_paragraph(readme_content)
    
    # Extract categories
    categories = extract_categories(readme_content)
    
    # Default metadata
    is_generated = False
    is_submitted = False
    is_extracted = False
    author_name = "James Utley PhD"  # Default author
    
    # Check meta.json if it exists
    if os.path.exists(meta_file):
        with open(meta_file, 'r', encoding='utf-8') as f:
            meta_json = json.load(f)
            
            # Update metadata from meta.json
            is_generated = meta_json.get('generated', False)
            is_submitted = meta_json.get('submitted', False)
            is_extracted = meta_json.get('extracted', False)
            
            # Get author if available
            if 'author' in meta_json:
                author_name = meta_json.get('author')
            
            # Update categories if available
            if 'categories' in meta_json and meta_json['categories']:
                categories = meta_json['categories']
    
    return {
        'slug': workflow_dir,
        'title': title,
        'description': description,
        'author_name': author_name,
        'json_content': workflow_json,
        'readme_content': readme_content,
        'categories': categories,
        'is_generated': is_generated,
        'is_submitted': is_submitted,
        'is_extracted': is_extracted
    }

def sync_workflow_to_database(workflow_data, supabase):
    """Add or update a workflow in the database"""
    try:
        # Call the database function
        result = supabase.rpc(
            'sync_workflow_to_database',
            {
                'p_slug': workflow_data['slug'],
                'p_title': workflow_data['title'],
                'p_description': workflow_data['description'],
                'p_author_name': workflow_data['author_name'],
                'p_json_content': workflow_data['json_content'],
                'p_readme_content': workflow_data['readme_content'],
                'p_categories': workflow_data['categories'],
                'p_is_generated': workflow_data['is_generated'],
                'p_is_submitted': workflow_data['is_submitted'],
                'p_is_extracted': workflow_data['is_extracted']
            }
        ).execute()
        
        if result.data and result.data.get('success'):
            print(f"  {result.data.get('operation')}: {workflow_data['slug']} (ID: {result.data.get('workflow_id')})")
            return True
        else:
            error = result.data.get('error') if result.data else 'Unknown error'
            print(f"  Error syncing workflow {workflow_data['slug']}: {error}")
            return False
            
    except Exception as e:
        print(f"  Exception syncing workflow {workflow_data['slug']}: {str(e)}")
        return False

def mark_workflow_deleted(slug, supabase):
    """Mark a workflow as deleted in the database"""
    try:
        result = supabase.rpc('mark_workflow_deleted', {'p_slug': slug}).execute()
        
        if result.data and result.data.get('success'):
            print(f"  Marked as deleted: {slug}")
            return True
        else:
            error = result.data.get('error') if result.data else 'Unknown error'
            print(f"  Error marking workflow as deleted {slug}: {error}")
            return False
            
    except Exception as e:
        print(f"  Exception marking workflow as deleted {slug}: {str(e)}")
        return False

def sync_workflows(full_sync=False, verbose=False):
    """Synchronize workflows between file system and database"""
    supabase = get_supabase_client()
    base_path = os.path.join(os.path.dirname(__file__), 'automation')
    
    if not os.path.exists(base_path):
        print(f"Error: Automation directory '{base_path}' does not exist.")
        return False
    
    # Get all workflow directories from filesystem
    try:
        workflow_dirs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
        workflow_dirs.sort()
    except Exception as e:
        print(f"Error reading workflow directories: {str(e)}")
        return False
    
    # Get all workflows from database
    try:
        db_workflows_response = supabase.table('workflows').select('id, slug').execute()
        db_workflows = {w['slug']: w['id'] for w in db_workflows_response.data}
    except Exception as e:
        print(f"Error fetching workflows from database: {str(e)}")
        return False
    
    fs_workflows = set(workflow_dirs)
    db_workflow_slugs = set(db_workflows.keys())
    
    # Workflows to add or update (in filesystem but not in DB, or in both)
    workflows_to_sync = fs_workflows
    
    # Workflows to mark as deleted (in DB but not in filesystem)
    workflows_to_delete = db_workflow_slugs - fs_workflows if full_sync else set()
    
    print(f"Found {len(workflows_to_sync)} workflows to sync and {len(workflows_to_delete)} to mark as deleted.")
    
    # Sync workflows
    success_count = 0
    for idx, workflow_dir in enumerate(workflows_to_sync, 1):
        if verbose:
            print(f"[{idx}/{len(workflows_to_sync)}] Processing: {workflow_dir}")
        
        workflow_data = get_workflow_from_filesystem(workflow_dir, base_path)
        if not workflow_data:
            print(f"  Skipping {workflow_dir}: Invalid workflow directory")
            continue
        
        if sync_workflow_to_database(workflow_data, supabase):
            success_count += 1
    
    # Mark deleted workflows
    deleted_count = 0
    for idx, slug in enumerate(workflows_to_delete, 1):
        if verbose:
            print(f"[{idx}/{len(workflows_to_delete)}] Marking as deleted: {slug}")
        
        if mark_workflow_deleted(slug, supabase):
            deleted_count += 1
    
    print(f"Synchronized {success_count}/{len(workflows_to_sync)} workflows.")
    if full_sync:
        print(f"Marked {deleted_count}/{len(workflows_to_delete)} workflows as deleted.")
    
    return True

def main():
    """Main entry point for the script"""
    parser = argparse.ArgumentParser(description="Workflow synchronization utility")
    parser.add_argument(
        "--full-sync", 
        action="store_true", 
        help="Perform a complete bidirectional sync, including marking workflows as deleted"
    )
    parser.add_argument(
        "--verbose", 
        action="store_true", 
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    print(f"Starting workflow synchronization at {datetime.datetime.now().isoformat()}")
    
    if sync_workflows(args.full_sync, args.verbose):
        print("Workflow synchronization completed successfully.")
    else:
        print("Workflow synchronization completed with errors.")
        sys.exit(1)

if __name__ == "__main__":
    main() 