# AI Frontiers Digest Workflow

An automated system that fetches and filters Hacker News stories, sending them to various platforms including Email and Discord.

## Features

- Fetches top stories from Hacker News API
- Filters stories based on configurable criteria (score, keywords)
- Concurrent processing using async/await
- Platform integrations:
  - Discord webhook integration for story notifications
  - Email newsletter
- Configurable filtering options
- Error handling and logging

## Prerequisites

- Python 3.11+
- Azure account (for deployment)
- Discord webhook URL
- Email credentials

## Installation

1. Clone the repository

```bash
git clone https://github.com/AICrafterZheng/AI-Frontiers-Digest-Workflow.git
```

2. Install dependencies

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Configure environment variables

```bash
cp .env.example .env
```
Edit .env with your credentials

## Usage

Deploy to Prefect Cloud:

```bash
python main.py
```

