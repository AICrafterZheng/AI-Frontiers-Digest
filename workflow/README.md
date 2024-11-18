# Hacker News Story Aggregator

An automated system that fetches and filters Hacker News stories, sending them to various platforms including Discord and Twitter.

## Features

- Fetches top stories from Hacker News API
- Filters stories based on configurable criteria (score, keywords)
- Concurrent processing using async/await
- Platform integrations:
  - Discord webhook integration for story notifications
  - Twitter posting capability
- Configurable filtering options
- Error handling and logging

## Prerequisites

- Python 3.9+
- Azure account (for deployment)
- Discord webhook URL
- Twitter API credentials

## Installation

1. Clone the repository

```bash
git clone [your-repo-url]
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Configure environment variables

```bash
cp .env.example .env
```
Edit .env with your credentials


## Usage

Run the application locally:

```bash
python main.py
```



## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request


## Resources

- [Hacker News API Documentation](https://github.com/HackerNews/API)
- [Azure Deployment Guide](https://learn.microsoft.com/en-us/azure/app-service/quickstart-python)
- [Discord Webhook Guide](https://discord.com/developers/docs/resources/webhook)

## License

[Your chosen license]
