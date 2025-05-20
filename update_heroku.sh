#!/bin/bash
# Update PewPew.buzz on Heroku with Auth0 changes

echo "Updating PewPew.buzz on Heroku with Auth0 integration..."

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
APP_NAME=${1:-"pewpew-buzz-9e1d6a9ed357"}
echo "Using app name: $APP_NAME"

# Set Git remote if not already set
if ! git remote | grep heroku &> /dev/null; then
    git remote add heroku "https://git.heroku.com/$APP_NAME.git"
    echo "Added Heroku remote"
else
    echo "Heroku remote already exists"
fi

# Update Auth0 environment variables if needed
read -p "Update Auth0 environment variables? (y/n): " UPDATE_AUTH0
if [[ $UPDATE_AUTH0 == "y" || $UPDATE_AUTH0 == "Y" ]]; then
    read -p "Enter your AUTH0_CLIENT_ID: " AUTH0_CLIENT_ID
    read -p "Enter your AUTH0_CLIENT_SECRET: " AUTH0_CLIENT_SECRET
    read -p "Enter your AUTH0_DOMAIN: " AUTH0_DOMAIN
    
    AUTH0_CALLBACK_URL="https://$APP_NAME.herokuapp.com/callback"
    
    echo "Setting Auth0 environment variables..."
    heroku config:set AUTH0_CLIENT_ID="$AUTH0_CLIENT_ID" --app "$APP_NAME"
    heroku config:set AUTH0_CLIENT_SECRET="$AUTH0_CLIENT_SECRET" --app "$APP_NAME"
    heroku config:set AUTH0_DOMAIN="$AUTH0_DOMAIN" --app "$APP_NAME"
    heroku config:set AUTH0_CALLBACK_URL="$AUTH0_CALLBACK_URL" --app "$APP_NAME"
fi

# Commit changes
git add app.py templates/ AUTH0_SETUP.md
git commit -m "Add Auth0 authentication and user profile"

# Deploy to Heroku
echo "Deploying to Heroku..."
git push heroku main

# Open the app
echo "Deployment complete! Opening app..."
heroku open --app "$APP_NAME"

echo "Remember to configure Auth0 settings as described in AUTH0_SETUP.md"
echo "Check logs with: heroku logs --tail --app $APP_NAME" 