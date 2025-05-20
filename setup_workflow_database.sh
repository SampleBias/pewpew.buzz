#!/bin/bash
# Setup script for workflow database system

set -e  # Exit on any error

# Set variables
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON_PATH=$(which python3)
LOG_DIR="$PROJECT_DIR/logs"
mkdir -p "$LOG_DIR"

# Function to check if running in Supabase
check_supabase() {
    echo "Checking if Supabase environment variables are set..."
    if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_KEY" ]; then
        echo "Error: SUPABASE_URL and SUPABASE_KEY must be set in your environment."
        echo "Please add them to your .env file or set them directly."
        exit 1
    fi
    echo "Supabase environment variables found."
}

# Function to execute an SQL file in Supabase
execute_sql_file() {
    local sql_file="$1"
    local description="$2"
    
    echo "Executing $description..."
    
    if [ ! -f "$sql_file" ]; then
        echo "Error: SQL file $sql_file not found."
        exit 1
    fi
    
    echo "This script will execute SQL from $sql_file in your Supabase database."
    echo "Please run this manually in the Supabase SQL editor or using their API."
    echo "Press Enter to continue or Ctrl+C to abort."
    read -r
    
    echo "SQL execution completed (manual step)."
}

# Main setup steps
echo "===== Workflow Database System Setup ====="
echo "This script will set up the workflow database system for pewpew.buzz."
echo

# Step 1: Check prerequisites
check_supabase

# Step 2: Create database schema
execute_sql_file "$PROJECT_DIR/supabase_schema_fixed.sql" "database schema script"

# Step 3: Create workflow synchronization function
execute_sql_file "$PROJECT_DIR/workflow_synchronization.sql" "workflow synchronization functions"

# Step 4: Migrate existing workflows to the database
echo "Migrating existing workflows to the database..."
"$PYTHON_PATH" "$PROJECT_DIR/workflow_sync.py" --full-sync --verbose
echo "Migration completed."

# Step 5: Set up regular synchronization
echo "Setting up regular synchronization..."
bash "$PROJECT_DIR/setup_workflow_sync_cron.sh"
echo "Regular synchronization setup completed."

echo
echo "===== Setup Completed Successfully! ====="
echo "Your workflow database system is now ready to use."
echo "Workflows will be synchronized hourly, and the database is now the primary source of truth."
echo
echo "If you need to do a manual synchronization, run:"
echo "  python workflow_sync.py --full-sync"
echo 