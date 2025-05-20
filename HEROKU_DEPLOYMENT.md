# PewPew.buzz Heroku Deployment Guide

This document explains how to deploy PewPew.buzz to Heroku.

## Prerequisites

1. A Heroku account
2. Heroku CLI installed locally
3. A Supabase account with project set up
4. Google Gemini API key

## Environment Variables

The following environment variables need to be set in your Heroku application:

```
FLASK_SECRET_KEY=<a-secure-random-string>
SUPABASE_URL=<your-supabase-url>
SUPABASE_KEY=<your-supabase-anon-key>
SUPABASE_SECRET_KEY=<your-supabase-service-role-key>
GEMINI_API_KEY=<your-google-gemini-api-key>
AUTH0_CLIENT_ID=<your-auth0-client-id>
AUTH0_CLIENT_SECRET=<your-auth0-client-secret>
AUTH0_DOMAIN=<your-auth0-domain>
AUTH0_CALLBACK_URL=<your-auth0-callback-url>
```

## Supabase Setup

Before deploying, ensure you have executed these SQL scripts in your Supabase SQL Editor:

1. `supabase_schema_fixed.sql` - Creates the database tables
2. `workflow_synchronization.sql` - Sets up synchronization functions
3. `add_workflow_ratings_policy.sql` - Adds required RLS policies

## Deployment Steps

1. Clone the repository
2. Set up Heroku:

```bash
heroku login
heroku create pewpew-buzz
```

3. Configure environment variables:

```bash
heroku config:set FLASK_SECRET_KEY=<your-secret-key>
heroku config:set SUPABASE_URL=<your-supabase-url>
heroku config:set SUPABASE_KEY=<your-supabase-anon-key>
heroku config:set SUPABASE_SECRET_KEY=<your-supabase-service-role-key>
heroku config:set GEMINI_API_KEY=<your-gemini-api-key>
heroku config:set AUTH0_CLIENT_ID=<your-auth0-client-id>
heroku config:set AUTH0_CLIENT_SECRET=<your-auth0-client-secret>
heroku config:set AUTH0_DOMAIN=<your-auth0-domain>
heroku config:set AUTH0_CALLBACK_URL=<your-app-url>/callback
```

4. Deploy the application:

```bash
git push heroku main
```

5. Open the application:

```bash
heroku open
```

## Post-Deployment Verification

1. Visit your app URL to verify the app is working
2. Check the logs for any errors:

```bash
heroku logs --tail
```

3. If the Supabase connection isn't working, verify your environment variables and SQL setup

## Troubleshooting

If you encounter any issues:

1. Check the Heroku logs: `heroku logs --tail`
2. Verify your environment variables: `heroku config`
3. Run the SQL installation check locally: `python check_sql_installation.py`
4. Test Supabase connection locally: `python test_supabase_connection.py` 