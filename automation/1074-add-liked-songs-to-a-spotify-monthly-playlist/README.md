# 1074 Add Liked Songs To A Spotify Monthly Playlist

Categories: AI, Marketing, Data Management, Content Creation, Engineering, IT, Project Management, Webhooks

This workflow automatically manages a monthly Spotify playlist by checking for new liked songs, adding them to the playlist, and ensuring the playlist is up-to-date in a NocoDb database.

Example: A music enthusiast could use this workflow to automatically maintain a monthly playlist of their favorite songs, without having to manually add new tracks each month. The workflow handles the entire process, from checking for new liked songs to updating the playlist in both Spotify and a NocoDb database.

## What You Can Do
- Automatically retrieves the last 10 liked songs from the user's Spotify account
- Checks if each song is already saved in the NocoDb database, and adds it if not
- Checks if the current month's playlist exists in Spotify and NocoDb, and creates it if not
- Adds any new songs to the current month's playlist in both Spotify and NocoDb
- Provides a centralized, up-to-date record of the user's monthly playlists in NocoDb

## Quick Start
1. Import this workflow to n8n
2. Configure your settings
3. Start automating!


