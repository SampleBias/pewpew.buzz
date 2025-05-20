# 2485 Automate Droplet Snapshots On Digitalocean

Categories: AI, Marketing, Data Management, Content Creation, Dev Ops, Engineering, IT, Project Management, Webhooks

This workflow automates the management of DigitalOcean Droplet snapshots by keeping the number of snapshots under a defined limit, deleting the oldest ones, and ensuring new snapshots are created at regular intervals.

Example: A business that runs multiple DigitalOcean Droplets could use this workflow to automatically manage their snapshots. It would ensure that they always have a recent backup of their Droplets, while also keeping the number of snapshots within a reasonable limit to save storage space.

## What You Can Do
- Runs every 48 hours to manage snapshots
- Retrieves a list of all Droplets and their existing snapshots
- Deletes the oldest snapshots if the number exceeds a defined limit (e.g., 4)
- Creates a new snapshot for each Droplet after cleaning up the old ones

## Quick Start
1. Import this workflow to n8n
2. Configure your settings
3. Start automating!


