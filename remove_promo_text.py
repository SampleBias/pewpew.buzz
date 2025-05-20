#!/usr/bin/env python3
import os
import re
import glob

def remove_promo_text_from_file(file_path):
    # The text to remove, with some regex escaping for special characters
    promo_text = re.compile(
        r'⚠️ WARNING: Stop Building Basic Automations For Peanuts\. 🚫\s*\n\s*'
        r'Here\'s the painful truth most won\'t tell you\.\.\.\s*\n\s*\n\s*'
        r'While 90% of builders are stuck selling \$500 n8n workflows \(and working way too hard\)\.\.\.\s*\n\s*'
        r'I\'m consistently closing \$6k-13k deals by doing ONE thing differently:\s*\n\s*'
        r'I combine simple automations with custom AI that takes less than a week to build\.\s*\n\s*\n\s*'
        r'Recent client wins:\s*\n\s*'
        r'\* Turned a basic invoicing headache into a \$6k project that saves my client 20 hours/week\s*\n\s*'
        r'\* Built a lead generation machine for law firms - they happily paid \$13k \(and it runs 24/7\)\s*\n\s*'
        r'\* Created AI-powered SEO automation that beats funded companies \(using \$0 in AI costs\)\s*\n\s*\n\s*'
        r'Time to build each solution\? Under 2 hours\.\s*\n\s*\n\s*'
        r'But here\'s what\'s crazy\.\.\.\s*\n\s*'
        r'Most automation builders think AI is "too complex" or "too expensive" to add to their stack\.\s*\n\s*'
        r'\(Meanwhile, I\'m charging 10x more for solutions that take the same time to build\)\s*\n\s*\n\s*'
        r'Want to see exactly how I do it\?\s*\n\s*'
        r'Inside our community, I show you:\s*\n\s*'
        r'\* The exact AI components that 3x your pricing overnight\s*\n\s*'
        r'\* My "\$15k Solution Stack" \(n8n \+ AI framework\)\s*\n\s*'
        r'\* Word-for-word scripts to close premium deals\s*\n\s*'
        r'\* Real examples of my \$10k\+ builds\s*\n\s*'
        r'\* The psychology behind why clients happily pay more\s*\n\s*\n\s*'
        r'Get your free trial here \(closing soon\): https://www\.skool\.com/masterclass-marketing'
    )
    
    try:
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Check if the promo text exists in the file
        if promo_text.search(content):
            # Remove the promotional text
            new_content = promo_text.sub('', content)
            
            # Write the updated content back to the file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            
            print(f"Successfully updated: {file_path}")
            return True
        else:
            print(f"No promotional text found in: {file_path}")
            return False
            
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return False

def main():
    # Get the base directory path - use the actual directory path
    base_dir = 'automation'
    
    # Check if the directory exists
    if not os.path.isdir(base_dir):
        print(f"Error: Directory '{base_dir}' not found.")
        return
    
    # Find all README.md files in the automation directory
    readme_files = glob.glob(f"{base_dir}/**/README.md", recursive=True)
    
    if not readme_files:
        print("No README.md files found in the automation directory.")
        return
    
    # Track statistics
    total_files = len(readme_files)
    updated_files = 0
    
    # Process each README.md file
    for file_path in readme_files:
        if remove_promo_text_from_file(file_path):
            updated_files += 1
    
    print(f"\nSummary: Updated {updated_files} out of {total_files} README.md files.")

if __name__ == "__main__":
    main() 