# 1997 Authenticate A User In A Workflow With Openid Connect

Categories: AI, Marketing, Data Management, Content Creation, Customer Support, Engineering, IT, Project Management, Webhooks

This workflow implements a secure OAuth 2.0 authentication flow, allowing users to log in to your application using an external identity provider.

Example: A web application that needs to authenticate users can use this workflow to integrate with an identity provider like Keycloak or Azure AD. Users can log in to the application using their existing credentials, and the workflow handles the necessary OAuth 2.0 handshake to obtain an access token for the user's profile information.

## What You Can Do
- Supports both PKCE (Proof Key for Code Exchange) and traditional OAuth 2.0 flows
- Retrieves user profile information from the identity provider's userinfo endpoint
- Provides a customizable login page and welcome page for the authenticated user
- Handles the complete OAuth 2.0 authorization code flow, including token exchange and error handling

## Quick Start
1. Import this workflow to n8n
2. Configure your settings
3. Start automating!


