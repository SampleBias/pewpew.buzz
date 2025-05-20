# Workflow Database Synchronization

This document explains how the workflow synchronization system works to keep the filesystem-based workflows in sync with the database.

## Overview

The pewpew.buzz platform uses both a filesystem-based approach and a database for storing automation workflows. To ensure consistency between these two storage mechanisms, we have implemented a synchronization system that:

1. Imports existing filesystem workflows into the database
2. Adds new workflows to the database when they are created
3. Updates workflows in the database when they are modified on the filesystem
4. Marks workflows as deleted in the database when they are removed from the filesystem

## Components

The synchronization system consists of the following components:

### 1. SQL Functions (`workflow_synchronization.sql`)

The SQL script creates the following database objects:

- `workflow_sync_log` table - Records all synchronization events for auditing
- `sync_workflow_to_database()` function - Adds or updates a workflow in the database
- `mark_workflow_deleted()` function - Marks a workflow as deleted/unpublished in the database

These functions handle all database operations in a consistent way, with proper error handling and transaction management.

### 2. Synchronization Script (`workflow_sync.py`)

This Python script handles the actual synchronization process:

- Reads workflow data from the filesystem
- Detects new, modified, and deleted workflows
- Calls the appropriate database functions to keep everything in sync
- Provides detailed logging of all operations

The script can be run in two modes:
- Regular sync: Only add new or update existing workflows
- Full sync: Also mark workflows as deleted if they no longer exist in the filesystem

### 3. Cron Job Setup (`setup_workflow_sync_cron.sh`)

This script sets up an hourly cron job to run the synchronization automatically. It:

- Creates necessary directories
- Sets up proper permissions
- Creates an hourly cron job
- Sets up logging

## How Workflows Are Managed

### File Structure

Each workflow in the filesystem is stored in a directory with the following structure:
- `workflow.json` - The actual workflow configuration
- `README.md` - Documentation and metadata for the workflow
- `meta.json` - Additional metadata including categories, author, etc.

### Database Structure

Workflows in the database are stored in the following tables:
- `workflows` - Main workflow data including JSON content and metadata
- `workflow_categories` - Categories for each workflow
- `workflow_ratings` - User ratings (thumbs up/down) for each workflow

## Usage

### Initial Migration

To perform the initial migration of all workflows from the filesystem to the database:

```bash
python workflow_sync.py --full-sync --verbose
```

### Automated Synchronization

Set up the automated hourly synchronization:

```bash
bash setup_workflow_sync_cron.sh
```

### Manual Synchronization

You can also run the synchronization manually at any time:

```bash
# Regular sync (add/update only)
python workflow_sync.py

# Full sync (add/update/delete)
python workflow_sync.py --full-sync

# Verbose output
python workflow_sync.py --verbose
```

## Troubleshooting

If you encounter issues with the synchronization:

1. Check the log file at `logs/workflow_sync.log`
2. Verify database connectivity and permissions
3. Ensure the SQL functions are properly installed in the database
4. Check that the filesystem permissions allow reading the workflow files

## Future Improvements

Potential future enhancements to the synchronization system:

1. Two-way synchronization (database changes reflected in filesystem)
2. Real-time synchronization using database triggers and webhooks
3. Conflict resolution for simultaneous edits
4. Version control and history tracking 