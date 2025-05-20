# 2576 Import Productboard Notes Companies And Features Into Snowflake

Categories: AI, Analytics, Marketing, Data Management, Content Creation, Ecommerce, Engineering, IT, Project Management, Webhooks

This workflow extracts data from Productboard, maps it to a Snowflake database, and sends a weekly update to Slack.

Example: A product manager could use this workflow to automatically sync Productboard data (features, notes, and companies) to a Snowflake data warehouse, and then send a weekly update to their team's Slack channel with key metrics like new insights added and unprocessed insights.

## What You Can Do
- Extracts data from Productboard's API, including features, notes, and companies
- Stores the data in a Snowflake database with separate tables for features, notes, and the relationship between notes and features
- Sends a weekly Slack message with a summary of new insights added and unprocessed insights
- Handles pagination and batching to efficiently process large amounts of data

## Quick Start
1. Import this workflow to n8n
2. Configure your settings
3. Start automating!


