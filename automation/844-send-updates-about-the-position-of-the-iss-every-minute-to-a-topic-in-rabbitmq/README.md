# 844 Send Updates About The Position Of The Iss Every Minute To A Topic In Rabbitmq

Categories: AI, Marketing, Data Management, Content Creation, Dev Ops, Ecommerce, Engineering, IT, Project Management, Webhooks

This workflow retrieves the current position of the International Space Station (ISS) from an API, processes the data, and publishes it to a RabbitMQ queue for further use.

Example: A space enthusiast or a company tracking the ISS could use this workflow to automatically monitor the location of the ISS and store the data in a RabbitMQ queue. This could be useful for applications that need to display the ISS's current position, analyze its movement patterns, or integrate the data into other systems.

## What You Can Do
- Periodically retrieves the current position of the ISS from an API
- Extracts relevant data (latitude, longitude, timestamp, and name) and stores it in a RabbitMQ queue
- Runs on a cron-based schedule, ensuring the data is updated regularly

## Quick Start
1. Import this workflow to n8n
2. Configure your settings
3. Start automating!


