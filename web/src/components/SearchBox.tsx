import { useState, useCallback } from 'react';
import { Search, X } from 'lucide-react';
import { Story } from '../types/types';
import { usePlayerStore } from '../store/usePlayerStore';

interface SearchBoxProps {
  onResultsFound?: (results: Story[], query: string) => void;
  className?: string;
}

export function SearchBox({ onResultsFound, className = '' }: SearchBoxProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const [searchError, setSearchError] = useState<string | null>(null);
  const setPlaylist = usePlayerStore(state => state.setPlaylist);

  const performSearch = useCallback(async () => {
    if (!searchQuery.trim()) {
      onResultsFound?.([], '');
      return;
    }

    setIsSearching(true);
    setSearchError(null);
    const apiUrl = import.meta.env.VITE_BACKEND_API_URL;

    try {
      const response = await fetch(`${apiUrl}/search?q=${encodeURIComponent(searchQuery)}`);
      if (!response.ok) {
        throw new Error('Search failed');
      }
      const data = await response.json();
      setPlaylist(data.audioTracks || []);
      onResultsFound?.(data.stories || [], searchQuery.trim());
    } catch (err) {
      setSearchError(err instanceof Error ? err.message : 'Search failed');
      onResultsFound?.([], searchQuery.trim());
    } finally {
      setIsSearching(false);
    }
  }, [searchQuery, onResultsFound, setPlaylist]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      performSearch();
    }
  };

  const clearSearch = () => {
    setSearchQuery('');
    onResultsFound?.([], '');
  };

  return (
    <div className={className}>
      <div className="max-w-2xl mx-auto">
        <div className="relative">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Search articles..."
            className="w-full px-4 py-2 pl-10 pr-4 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:text-white hover:border-blue-500 dark:hover:border-blue-400 transition-colors duration-200"
          />
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
          {searchQuery && !isSearching && (
            <button
              onClick={clearSearch}
              className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors duration-200"
            >
              <X className="w-4 h-4" />
            </button>
          )}
          {isSearching && (
            <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-400"></div>
            </div>
          )}
        </div>
      </div>
      {searchError && (
        <div className="mt-4 text-center text-red-500">{searchError}</div>
      )}
    </div>
  );
}
