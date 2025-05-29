# Technical_Analyst_Agent.json

Categories: Analytics

This Telegram-based agent interprets financial questions and stock tickers, performing technical chart analysis using a toolchain that generates TradingView-style charts with MACD and volume indicators. It then provides a visual chart and expert analysis (including candlestick patterns, support/resistance, and MACD insights) directly to the user in an approachable, professional tone—without offering direct financial advice.

## Technical Details

This workflow consists of 15 nodes that work together to automate your process. Here's what it uses:

- @n8n/n8n-nodes-langchain.lmChatAnthropic: Anthropic Chat Model
- @n8n/n8n-nodes-langchain.memoryBufferWindow: Window Buffer Memory
- @n8n/n8n-nodes-langchain.toolWorkflow: Get Chart
- @n8n/n8n-nodes-langchain.agent: AI Agent
- telegramTrigger: Telegram Trigger
- telegram: Send Analysis, Send Chart
- stickyNote: Sticky Note, Sticky Note1
- executeWorkflowTrigger: Workflow Input Trigger
- set: response, Set Ticker
- @n8n/n8n-nodes-langchain.openAi: Technical Analysis
- httpRequest: Download Chart, Get Chart URL

## Usage

1. Download the workflow JSON file
2. Import it into your n8n instance
3. Review and adjust the workflow as needed
4. Activate and test the workflow

