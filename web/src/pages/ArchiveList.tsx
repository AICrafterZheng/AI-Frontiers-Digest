import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Archive } from 'lucide-react';

interface NewsStats {
  [date: string]: {
    hackernews: number;
    techcrunch: number;
    latentspace: number;
  };
}

export const ArchiveList = () => {
  const [stats, setStats] = useState<NewsStats>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const apiUrl = import.meta.env.VITE_BACKEND_API_URL;
        const response = await fetch(`${apiUrl}/news-stats`);
        if (!response.ok) throw new Error('Failed to fetch stats');
        const data = await response.json();
        setStats(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  const content = (
    <div className="space-y-4">
      {Object.entries(stats).map(([date, sources]) => (
        <Link
          to={`/articles?date=${encodeURIComponent(date)}`}
          key={date} 
          className="block border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
        >
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              {date}
            </h3>
            <div className="flex gap-4 text-sm text-gray-600 dark:text-gray-400">
              {sources.hackernews > 0 && <span>Hacker News: {sources.hackernews}</span>}
              {sources.techcrunch > 0 && <span>TechCrunch: {sources.techcrunch}</span>}
              {sources.latentspace > 0 && <span>Latent Space: {sources.latentspace}</span>}
            </div>
          </div>
        </Link>
      ))}
    </div>
  );

  if (loading) return (
    <div className="container mx-auto px-4">
      <div className="flex items-center gap-2 mb-6">
        <Archive className="w-6 h-6 text-gray-900 dark:text-white" />
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">News Archive</h1>
      </div>
      <div className="text-center text-gray-600 dark:text-gray-400">Loading archive...</div>
    </div>
  );

  if (error) return (
    <div className="container mx-auto px-4">
      <div className="flex items-center gap-2 mb-6">
        <Archive className="w-6 h-6 text-gray-900 dark:text-white" />
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">News Archive</h1>
      </div>
      <div className="text-center text-red-600 dark:text-red-400">{error}</div>
    </div>
  );

  return (
    <div className="container mx-auto px-4">
      <div className="flex items-center gap-2 mb-6">
        <Archive className="w-6 h-6 text-gray-900 dark:text-white" />
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">News Archive</h1>
      </div>

      {/* Mobile view */}
      <div className="sm:hidden">
        {content}
      </div>

      {/* Desktop view with background */}
      <div className="hidden sm:block bg-white dark:bg-gray-800 shadow-md rounded-lg overflow-hidden">
        <div className="p-6">
          {content}
        </div>
      </div>
    </div>
  );
};