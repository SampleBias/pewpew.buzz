#!/usr/bin/env python3
import os
import re
import json

# Define categories
CATEGORIES = [
    'AI', 'Analytics', 'Marketing', 'Data Management', 'Email', 'Content Creation', 
    'Customer Support', 'Dev Ops', 'Ecommerce', 'Education', 'Engineering', 'Finance', 
    'HR', 'IT', 'Project Management', 'Social Media', 'Webhooks', 'FEATURED'
]

DEFAULT_CATEGORY = 'Uncategorized'

# Keywords for each category
CATEGORY_KEYWORDS = {
    'AI': ['ai', 'artificial intelligence', 'machine learning', 'ml', 'gpt', 'openai', 'llm', 'chatgpt', 'chatbot', 'nlp'],
    'Analytics': ['analytics', 'metrics', 'statistics', 'reporting', 'data analysis', 'dashboard', 'chart', 'graph', 'measure'],
    'Marketing': ['marketing', 'campaign', 'leads', 'seo', 'social media', 'advertising', 'email campaign', 'branding'],
    'Data Management': ['data', 'database', 'storage', 'csv', 'json', 'spreadsheet', 'import', 'export', 'mysql', 'postgres', 'data extraction'],
    'Email': ['email', 'newsletter', 'smtp', 'imap', 'inbox', 'mail', 'gmail', 'outlook'],
    'Content Creation': ['content', 'blog', 'article', 'create', 'generate', 'writing', 'image generation', 'content management'],
    'Customer Support': ['customer support', 'ticket', 'helpdesk', 'support', 'customer service', 'inquiry', 'faq'],
    'Dev Ops': ['devops', 'deployment', 'pipeline', 'git', 'github', 'ci/cd', 'monitoring', 'logging', 'backup'],
    'Ecommerce': ['ecommerce', 'shop', 'store', 'product', 'payment', 'cart', 'order', 'shopify', 'woocommerce'],
    'Education': ['education', 'learning', 'teaching', 'course', 'student', 'school', 'training'],
    'Engineering': ['engineering', 'code', 'development', 'api', 'integration', 'technical', 'software', 'build'],
    'Finance': ['finance', 'accounting', 'invoice', 'payment', 'banking', 'transaction', 'money', 'budget'],
    'HR': ['hr', 'human resources', 'recruiting', 'hiring', 'employee', 'onboarding', 'payroll', 'benefits'],
    'IT': ['it', 'infrastructure', 'network', 'security', 'system', 'server', 'cloud', 'vpn'],
    'Project Management': ['project management', 'task', 'project', 'planning', 'team', 'collaboration', 'workflow', 'jira', 'asana', 'trello'],
    'Social Media': ['social media', 'twitter', 'facebook', 'instagram', 'linkedin', 'post', 'social', 'tweet'],
    'Webhooks': ['webhook', 'http', 'trigger', 'endpoint', 'callback', 'request', 'response', 'api'],
    'FEATURED': ['featured']
}

def categorize_readme(content):
    """Determine categories based on README content."""
    content = content.lower()
    
    # Check for preset categories in the README
    category_match = re.search(r'categories:\s*(.*?)$', content, re.MULTILINE)
    if category_match:
        existing_categories = [c.strip() for c in category_match.group(1).split(',')]
        # Filter out any that aren't in our list
        return [c for c in existing_categories if c in CATEGORIES or c.upper() in CATEGORIES]
    
    # Match by keywords
    matched_categories = []
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in content:
                matched_categories.append(category)
                break
    
    # If no categories matched, use default
    if not matched_categories:
        return [DEFAULT_CATEGORY]
    
    return matched_categories

def add_categories_to_readme(readme_path, categories):
    """Add categories to README.md file."""
    with open(readme_path, 'r') as f:
        content = f.read()
    
    # Check if Categories line already exists
    if re.search(r'categories:', content, re.IGNORECASE):
        # Replace existing Categories line
        content = re.sub(r'categories:.*?$', f'Categories: {", ".join(categories)}', content, flags=re.IGNORECASE|re.MULTILINE)
    else:
        # Add Categories line after title
        title_end = content.find('\n', content.find('#'))
        if title_end != -1:
            content = content[:title_end+1] + f'\nCategories: {", ".join(categories)}\n' + content[title_end+1:]
    
    with open(readme_path, 'w') as f:
        f.write(content)

def create_meta_json(folder_path, categories):
    """Create or update meta.json file with categories."""
    meta_path = os.path.join(folder_path, 'meta.json')
    meta_data = {}
    
    if os.path.exists(meta_path):
        with open(meta_path, 'r') as f:
            try:
                meta_data = json.load(f)
            except json.JSONDecodeError:
                meta_data = {}
    
    meta_data['categories'] = categories
    
    with open(meta_path, 'w') as f:
        json.dump(meta_data, f, indent=2)

def process_automations():
    base_path = os.path.join(os.path.dirname(__file__), 'automation')
    
    # Check if path exists
    if not os.path.exists(base_path):
        print(f"Error: {base_path} does not exist.")
        return
    
    print(f"Processing automations in {base_path}...")
    processed = 0
    for folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder)
        if not os.path.isdir(folder_path):
            continue
        
        readme_path = os.path.join(folder_path, 'README.md')
        if not os.path.exists(readme_path):
            continue
        
        with open(readme_path, 'r') as f:
            content = f.read()
        
        categories = categorize_readme(content)
        
        # Add FEATURED to popular workflows (optional)
        if 'FEATURED' not in categories and ('popular' in content.lower() or 'featured' in content.lower()):
            categories.append('FEATURED')
        
        print(f"{folder}: {', '.join(categories)}")
        
        # Update README.md with categories
        add_categories_to_readme(readme_path, categories)
        
        # Create meta.json with categories
        create_meta_json(folder_path, categories)
        processed += 1
    
    print(f"Processed {processed} automation folders.")

if __name__ == "__main__":
    process_automations() 