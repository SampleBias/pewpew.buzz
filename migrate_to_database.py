#!/usr/bin/env python3
"""
Migration script to transfer existing file-based workflows to the Supabase database.
"""

import os
import json
import re
import datetime
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

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

def migrate_workflows():
    """Migrate existing workflows from files to the database"""
    base_path = os.path.join(os.path.dirname(__file__), 'automation')
    
    if not os.path.exists(base_path):
        print(f"Error: Automation directory '{base_path}' does not exist.")
        return
    
    # Get all workflow directories
    workflow_dirs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    
    # Sort workflows to maintain order
    workflow_dirs.sort()
    
    print(f"Found {len(workflow_dirs)} workflows to migrate.")
    
    for idx, workflow_dir in enumerate(workflow_dirs, 1):
        try:
            dir_path = os.path.join(base_path, workflow_dir)
            
            # Required files
            workflow_file = os.path.join(dir_path, 'workflow.json')
            readme_file = os.path.join(dir_path, 'README.md')
            meta_file = os.path.join(dir_path, 'meta.json')
            
            if not os.path.exists(workflow_file) or not os.path.exists(readme_file):
                print(f"Skipping {workflow_dir}: Missing required files")
                continue
            
            print(f"[{idx}/{len(workflow_dirs)}] Migrating: {workflow_dir}")
            
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
            
            # Determine if workflow was generated by AI or submitted by a user
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
            
            # Get or create workflow in database
            workflow_data = {
                'slug': workflow_dir,
                'title': title,
                'description': description,
                'author_name': author_name,
                'json_content': workflow_json,
                'readme_content': readme_content,
                'is_generated': is_generated,
                'is_submitted': is_submitted,
                'is_extracted': is_extracted,
                'published': True,
                'published_date': datetime.datetime.now().isoformat()
            }
            
            # Insert the workflow
            result = supabase.table('workflows').insert(workflow_data).execute()
            
            if not result.data:
                print(f"  Error inserting workflow: {workflow_dir}")
                continue
                
            workflow_id = result.data[0]['id']
            print(f"  Inserted workflow ID: {workflow_id}")
            
            # Insert categories
            for category in categories:
                supabase.table('workflow_categories').insert({
                    'workflow_id': workflow_id,
                    'category': category
                }).execute()
            
            print(f"  Added {len(categories)} categories")
            
            # Get existing ratings
            try:
                ratings_response = supabase.table('workflow_ratings').select('*').eq('workflow_id', workflow_dir).execute()
                
                if not ratings_response.data:
                    # Create initial ratings entry
                    supabase.table('workflow_ratings').insert({
                        'workflow_id': workflow_dir,
                        'upvotes': 0,
                        'downvotes': 0
                    }).execute()
                    print("  Created default ratings")
            except Exception as e:
                print(f"  Error handling ratings: {str(e)}")
            
            print(f"  Successfully migrated: {workflow_dir}")
            
        except Exception as e:
            print(f"Error migrating {workflow_dir}: {str(e)}")
    
    print("Migration completed!")

if __name__ == "__main__":
    migrate_workflows() 