#!/bin/bash
# Setup script for workflow synchronization cron job

# Set variables
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON_PATH=$(which python3)
WORKFLOW_SYNC_SCRIPT="$PROJECT_DIR/workflow_sync.py"
LOG_DIR="$PROJECT_DIR/logs"
LOG_FILE="$LOG_DIR/workflow_sync.log"

# Create logs directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Make the script executable
chmod +x "$WORKFLOW_SYNC_SCRIPT"

# Create the cron entry - run every hour
CRON_ENTRY="0 * * * * cd $PROJECT_DIR && $PYTHON_PATH $WORKFLOW_SYNC_SCRIPT --full-sync >> $LOG_FILE 2>&1"

# Add to crontab if not already there
(crontab -l 2>/dev/null | grep -v "$WORKFLOW_SYNC_SCRIPT" ; echo "$CRON_ENTRY") | crontab -

# Check if crontab was updated successfully
if [ $? -eq 0 ]; then
    echo "Cron job setup successfully! Workflow synchronization will run hourly."
    echo "Logs will be written to $LOG_FILE"
    echo "Current crontab entries:"
    crontab -l
else
    echo "Failed to setup cron job. Please check permissions and try again."
    exit 1
fi

echo "Would you like to run the initial workflow synchronization now? (y/n)"
read -r run_now

if [[ $run_now =~ ^[Yy]$ ]]; then
    echo "Running initial workflow synchronization..."
    "$PYTHON_PATH" "$WORKFLOW_SYNC_SCRIPT" --full-sync --verbose
    echo "Initial synchronization complete."
fi

echo "Setup completed successfully!" 