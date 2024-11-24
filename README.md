# AI Frontiers Digest

**AI Frontiers Digest** leverages Large Language Models (LLMs) to intelligently summarize and curate the latest developments in artificial intelligence. By analyzing both articles and article discussions, it provides concise, digestible insights into the AI landscape. Additionally, it generates podcasts and audio from articles, which provides a more engaging and immersive experience.

## Project Structure

- `/web` - Frontend application (Vite + React + TypeScript)
- `/workflow` - Prefect workflows for fetching, processing, and summarizing news articles

## Key Features

1. **AI News Aggregation:** Automatically fetch and organize AI news from trusted sources
 - Hacker News
   - We filter for stories mentioning keywords: "gpt, llm, workflow, serverless, function as a service, backend as a service, faas, baas, developer experience, developer productivity, dev productivity, dev experience,  automation, ai, artificial intelligence, dev, dx, machine learning, deep learning, nlp, openai, anthropic, gemini, claude, devin, mistral, llama, sora, midjourney, lpu, LlamaIndex, LangChain"
 - TechCrunch AI
   - We scrape the [TechCrunch AI section](https://techcrunch.com/category/artificial-intelligence/) for the latest articles. 
- Right now, Hacker News and TechCrunch AI articles are supported, actively adding more resources.
2. **Summarization:** Summarize articles and Hacker News discussions
3. **Email Delivery:** Deliver summaries directly to your inbox
4. **Discord Delivery:** Deliver summaries to our [Discord community](https://discord.gg/Ukbeb8rDmm)
5. **Web App:** View summaries and explore AI news on [aicrafter.info](https://aicrafter.info)
6. **Audio:** Generate audio from article.
6. **Podcast:** Generate podcasts from article.


## Tech Stack

### Frontend
- Vite
- React
- TypeScript
- TailwindCSS

### Backend
- Prefect (Workflow orchestration)
- Supabase (Database + Audio Storage)
- Cloudflare Page Functions (Backend APIs)
- Azure
  - Azure Container Registry (Docker Images for Prefect Workers Pool)
  - Azure AI Services (LLMs)
  - Azure TTS (Text-to-Speech)
- Jina Reader (URL to markdown)
- NotebookLM (Article to Podcast)
    - Credits to [NotebookLlama](https://github.com/meta-llama/llama-recipes/blob/main/recipes/quickstart/NotebookLlama/README.md) for transcript generation, and [PodCastLM](https://github.com/YOYZHANG/PodCastLM/blob/master/backend/utils.py) for audio generation.
    - Transcript generation model: Azure AI Services (gpt-4o-mini)
    - Audio generation: Azure TTS
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

- Add more sources:
  - Github
  - Twitter
  - Reddit
  - Product Hunt
  - LinkedIn
- Add Audio playlist to auto-play next audio.

Let me know what do you like to see! Join our [Discord](https://discord.gg/Ukbeb8rDmm).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Built with ❤️ by [dannyzheng.me](https://dannyzheng.me) for the AI community.