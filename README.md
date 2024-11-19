# AI Frontiers Digest

**AI Frontiers Digest** leverages Large Language Models (LLMs) to intelligently summarize and curate the latest developments in artificial intelligence. By analyzing both articles and Hacker News discussions, it provides concise, digestible insights into the AI landscape.

## Project Structure

- `/web` - Frontend application (Vite + React + TypeScript)
- `/workflow` - Prefect workflows for fetching, processing, and summarizing news articles

## Key Features

1. **AI News Aggregation:** Automatically fetch and organize AI news from trusted sources
- Right now, only Hacker News and TechCrunch AI articles are supported. We will add more sources in the future.
2. **Summarization:** Summarize articles and Hacker News discussions
3. **Email Delivery:** Deliver summaries directly to your inbox
4. **Discord Delivery:** Deliver summaries to our [Discord community](https://discord.gg/Ukbeb8rDmm)
5. **Web App:** View summaries and explore AI news on [aicrafter.info](https://aicrafter.info)


## Tech Stack

### Frontend
- Vite (Build tool)
- React
- TypeScript
- Modern CSS (TailwindCSS/styled-components)

### Backend
- Prefect (Workflows)
- Supabase (Database)
- Cloudflare Page Functions (Backend APIs)
- Azure Container Registry (Docker Images)
- Azure AI Services (LLMs)
- OpenRouter (LLMs)
- Resend (Email)

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/your-username/ai-frontiers-digest.git
cd ai-frontiers-digest
```

2. Install dependencies:
```bash
cd web
npm install
```

3. Start the Web App:
```bash
npm run dev
```

4. Start Cloudflare Page Functions (Backend APIs):
```bash
npm run preview:wrangler
```

## Milestones

- [ ] Add more sources (e.g. Twitter, Reddit, etc.)
- [ ] Add more summarization options (e.g. NotebookLM Podcast, audio, etc.)


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Built with ❤️ by [dannyzheng.me](https://dannyzheng.me) for the AI community.