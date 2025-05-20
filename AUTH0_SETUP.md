# Auth0 Setup Guide for PewPew.buzz

This guide explains how to configure Auth0 for PewPew.buzz on Heroku.

## 1. Create an Auth0 Account and Application

1. Sign up for an Auth0 account at [auth0.com](https://auth0.com/)
2. Create a new application:
   - Go to Applications > Applications
   - Click "Create Application"
   - Name it "PewPew Buzz"
   - Select "Regular Web Applications"
   - Click "Create"

## 2. Configure Application Settings

### Application URLs

For your application deployed at `https://pewpew-buzz-9e1d6a9ed357.herokuapp.com/`, configure the following URLs:

1. **Allowed Callback URLs**:
   ```
   https://pewpew-buzz-9e1d6a9ed357.herokuapp.com/callback
   ```

2. **Allowed Logout URLs**:
   ```
   https://pewpew-buzz-9e1d6a9ed357.herokuapp.com/
   https://pewpew-buzz-9e1d6a9ed357.herokuapp.com/dashboard
   ```

3. **Allowed Web Origins**:
   ```
   https://pewpew-buzz-9e1d6a9ed357.herokuapp.com
   ```

4. **Allowed Origins (CORS)**:
   ```
   https://pewpew-buzz-9e1d6a9ed357.herokuapp.com
   ```

### Advanced Settings

1. Grant Types:
   - Authorization Code
   - Implicit
   - Refresh Token

2. JWT Expiration: 
   - Set to 86400 seconds (24 hours) or your preferred duration

## 3. Update Heroku Environment Variables

Set the following environment variables in your Heroku app:

```bash
heroku config:set AUTH0_CLIENT_ID=your_client_id --app pewpew-buzz-9e1d6a9ed357
heroku config:set AUTH0_CLIENT_SECRET=your_client_secret --app pewpew-buzz-9e1d6a9ed357
heroku config:set AUTH0_DOMAIN=your_auth0_domain.auth0.com --app pewpew-buzz-9e1d6a9ed357
heroku config:set AUTH0_CALLBACK_URL=https://pewpew-buzz-9e1d6a9ed357.herokuapp.com/callback --app pewpew-buzz-9e1d6a9ed357
```

## 4. Configure Social Connections (Optional)

1. Go to Authentication > Social in the Auth0 dashboard
2. Enable the social logins you want (Google, GitHub, etc.)
3. Configure the required credentials for each provider

## 5. Customize Login Page (Optional)

1. Go to Authentication > Login Experience
2. Customize the look and feel of the login page to match PewPew.buzz's style

## 6. Test the Login Flow

1. Visit your deployed app at `https://pewpew-buzz-9e1d6a9ed357.herokuapp.com/`
2. Click on "Login"
3. You should be redirected to the Auth0 login page
4. After logging in, you should be redirected back to your profile page

## Troubleshooting

If you encounter any issues:

1. Check that the callback URL exactly matches what's in your Auth0 settings
2. Verify all environment variables are set correctly
3. Look at the application logs in Heroku: `heroku logs --tail --app pewpew-buzz-9e1d6a9ed357`
4. Check the Auth0 logs in the Auth0 dashboard under Monitoring > Logs 