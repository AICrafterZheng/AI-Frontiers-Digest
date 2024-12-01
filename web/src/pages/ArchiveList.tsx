import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

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

  if (loading) return (
    <div className="flex justify-center items-center min-h-[60vh]">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900 dark:border-white"></div>
    </div>
  );
  if (error) return (
    <div className="text-center py-12">
      <p className="text-red-600 dark:text-red-400">{error}</p>
    </div>
  );

  return (
    <div className="max-w-4xl mx-auto p-6 dark:bg-gray-900">
      <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">News Archive</h1>
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
    </div>
  );
};