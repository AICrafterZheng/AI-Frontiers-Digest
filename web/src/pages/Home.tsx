import NewsCategory from '../components/NewsCategory';
import { Package2, Github } from 'lucide-react';

// Custom YCombinator icon since it's not in lucide-react
function YCombinatorIcon() {
  return (
    <svg viewBox="0 0 24 24" className="w-6 h-6 text-white" fill="currentColor">
      <path d="M0 24V0h24v24H0zM6.951 5.896l4.112 7.708v5.064h1.583v-4.972l4.148-7.799h-1.749l-2.457 4.875c-.372.745-.688 1.434-.688 1.434s-.297-.708-.651-1.434L8.831 5.896h-1.88z" />
    </svg>
  );
}

export default function Home() {
  const hackerNewsItems = [
    {
      id: 1,
      title: "Everything Is Just Functions: Mind-Blowing Insights from SICP",
      points: 128,
      slug: "sicp-insights"
    },
    {
      id: 2,
      title: "Cone of Shame Cat Lamp",
      points: 6,
      slug: "cat-lamp"
    },
    // Add more items as needed
  ];

  const productHuntItems = [
    {
      id: 1,
      title: "AI Game Master — Fully immersive DnD experience",
      points: 289,
      slug: "ai-game-master"
    },
    {
      id: 2,
      title: "Momen — Build your MVP and scale it, no code needed.",
      points: 305,
      slug: "momen-mvp"
    },
    // Add more items as needed
  ];

  const githubItems = [
    {
      id: 1,
      title: "DataExpert-io / data-engineer-handbook",
      stars: 14973,
      slug: "data-engineer-handbook"
    },
    {
      id: 2,
      title: "GoogleCloudPlatform / generative-ai",
      stars: 7806,
      slug: "google-gen-ai"
    },
    // Add more items as needed
  ];

  return (
    <main className="relative pt-24 px-4 pb-16">
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <NewsCategory 
          title="Hacker News"
          icon={<YCombinatorIcon />}
          lastUpdate="47分钟前更新"
          backgroundColor="bg-[#ff6600]"
          items={hackerNewsItems}
        />

        <NewsCategory 
          title="Product Hunt"
          icon={<Package2 className="w-6 h-6 text-white" />}
          lastUpdate="30分钟前更新"
          backgroundColor="bg-[#da552f]"
          items={productHuntItems}
        />

        <NewsCategory 
          title="Github Today"
          icon={<Github className="w-6 h-6 text-white" />}
          lastUpdate="21分钟前更新"
          backgroundColor="bg-[#333]"
          items={githubItems}
        />
      </div>
    </main>
  );
}