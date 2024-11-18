# AI Frontiers Digest

**AI Frontiers Digest** leverages Large Language Models (LLMs) to intelligently summarize and curate the latest developments in artificial intelligence. By analyzing both articles and Hacker News discussions, it provides concise, digestible insights into the AI landscape.

## Project Structure

- `/web` - Frontend application (Vite + React + TypeScript)
- `/workflow` - Prefect workflows for fetching, processing, and summarizing news articles

## Key Features

1. **Real-time AI News Aggregation:** Automatically fetch and organize AI news from trusted sources
2. **Modern Web Architecture:**
   - Server-side rendering for optimal performance
   - Edge computing via Cloudflare Workers
   - TypeScript for enhanced code reliability
3. **Responsive Design:** Mobile-first approach ensuring great UX across all devices
4. **AI Content Curation:** Smart filtering and categorization of AI-related content

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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Built with ❤️ by [dannyzheng.me](https://dannyzheng.me) for the AI community