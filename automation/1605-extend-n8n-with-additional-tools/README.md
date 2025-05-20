# 1605 Extend N8N With Additional Tools

Categories: AI, Marketing, Data Management, Content Creation, Engineering, IT, Project Management, Webhooks

This workflow is a Telegram bot that allows users to request weather information for several European capitals, with the data displayed in an image generated using the R programming language.

Example: A user could interact with the bot by sending the "/getweather" command, which would trigger the workflow to fetch weather data from the OpenWeatherMap API, process the data in R, and send the resulting image back to the user via Telegram.

## What You Can Do
- Handles different bot commands (e.g., "/start", "/getweather") using a switch node
- Fetches weather data from the OpenWeatherMap API and processes it in R to generate an image
- Provides error handling for both API and R script failures, with appropriate error messages sent to the user

## Quick Start
1. Import this workflow to n8n
2. Configure your settings
3. Start automating!


