# 1073 Scrape And Store Data From Multiple Website Pages

Categories: AI, Marketing, Data Management, Content Creation, Ecommerce, Engineering, Finance, HR, IT, Project Management, Webhooks

This workflow scrapes SWIFT code data from a website, normalizes the country names, and stores the data in a MongoDB database.

Example: A financial institution or payment processing company might use this workflow to automatically gather and maintain a comprehensive database of SWIFT codes, which are essential for international wire transfers and other financial transactions.

## What You Can Do
- Extracts a list of countries from a website and iterates through them to scrape SWIFT code data
- Normalizes the country names using the uProc service to ensure consistent data
- Stores the scraped data (SWIFT codes, bank names, cities, etc.) in a MongoDB database
- Handles pagination and caching of HTML files to avoid redundant requests

## Quick Start
1. Import this workflow to n8n
2. Configure your settings
3. Start automating!


