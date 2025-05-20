#!/bin/bash
# Deploy PewPew.buzz to Heroku

echo "Preparing to deploy PewPew.buzz to Heroku..."

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "Heroku CLI not found. Please install it first."
    echo "Visit: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Check if user is logged in to Heroku
heroku whoami &> /dev/null
if [ $? -ne 0 ]; then
    echo "You are not logged in to Heroku. Please log in first:"
    heroku login
fi

# Check if app name is provided
APP_NAME=${1:-"pewpew-buzz"}
echo "Using app name: $APP_NAME"

# Check if app exists, if not create it
heroku apps:info "$APP_NAME" &> /dev/null
if [ $? -ne 0 ]; then
    echo "Creating Heroku app: $APP_NAME"
    heroku create "$APP_NAME"
else
    echo "Heroku app $APP_NAME already exists"
fi

# Set Git remote if not already set
if ! git remote | grep heroku &> /dev/null; then
    git remote add heroku "https://git.heroku.com/$APP_NAME.git"
    echo "Added Heroku remote"
else
    echo "Heroku remote already exists"
fi

# Prompt for environment variables
read -p "Enter your SUPABASE_URL: " SUPABASE_URL
read -p "Enter your SUPABASE_KEY (anon key): " SUPABASE_KEY
read -p "Enter your SUPABASE_SECRET_KEY (service role key): " SUPABASE_SECRET_KEY
read -p "Enter your GEMINI_API_KEY: " GEMINI_API_KEY
read -p "Enter your AUTH0_CLIENT_ID (or leave blank if not using Auth0): " AUTH0_CLIENT_ID
read -p "Enter your AUTH0_CLIENT_SECRET (or leave blank if not using Auth0): " AUTH0_CLIENT_SECRET
read -p "Enter your AUTH0_DOMAIN (or leave blank if not using Auth0): " AUTH0_DOMAIN

# Generate a random Flask secret key
FLASK_SECRET_KEY=$(openssl rand -hex 24)
echo "Generated random FLASK_SECRET_KEY"

# Set AUTH0_CALLBACK_URL based on the app URL
AUTH0_CALLBACK_URL="https://$APP_NAME.herokuapp.com/callback"

# Set environment variables
echo "Setting environment variables..."
heroku config:set FLASK_SECRET_KEY="$FLASK_SECRET_KEY" --app "$APP_NAME"
heroku config:set SUPABASE_URL="$SUPABASE_URL" --app "$APP_NAME"
heroku config:set SUPABASE_KEY="$SUPABASE_KEY" --app "$APP_NAME"
heroku config:set SUPABASE_SECRET_KEY="$SUPABASE_SECRET_KEY" --app "$APP_NAME"
heroku config:set GEMINI_API_KEY="$GEMINI_API_KEY" --app "$APP_NAME"

# Only set Auth0 variables if provided
if [ -n "$AUTH0_CLIENT_ID" ]; then
    heroku config:set AUTH0_CLIENT_ID="$AUTH0_CLIENT_ID" --app "$APP_NAME"
    heroku config:set AUTH0_CLIENT_SECRET="$AUTH0_CLIENT_SECRET" --app "$APP_NAME"
    heroku config:set AUTH0_DOMAIN="$AUTH0_DOMAIN" --app "$APP_NAME"
    heroku config:set AUTH0_CALLBACK_URL="$AUTH0_CALLBACK_URL" --app "$APP_NAME"
fi

# Commit any changes
git add Procfile runtime.txt requirements.txt .slugignore
git diff-index --quiet HEAD || git commit -m "Prepare for Heroku deployment"

# Deploy to Heroku
echo "Deploying to Heroku..."
git push heroku main

# Open the app
echo "Deployment complete! Opening app..."
heroku open --app "$APP_NAME"

echo "Remember to run the SQL scripts in your Supabase project:"
echo "1. supabase_schema_fixed.sql"
echo "2. workflow_synchronization.sql"
echo "3. add_workflow_ratings_policy.sql"

echo "Check logs with: heroku logs --tail --app $APP_NAME" 