import { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom';
import { NewsletterCard } from '../components/NewsletterCard';
import { SearchBox } from '../components/SearchBox';
import { Story, NewsletterProps } from "../types/types";
import { usePlayerStore } from '../store/usePlayerStore';

const getSubtitle = (countBySource: Record<string, number>) => {
  let subtitle = 'Today, our AI agents found '
  if (countBySource.hackernews !== undefined) {
    subtitle += `${countBySource.hackernews} Hacker News`
  }

  if (countBySource.hackernews !== undefined && countBySource.techcrunch !== undefined) {
    subtitle += ' and '
  }

  if (countBySource.techcrunch !== undefined) {
    subtitle += `${countBySource.techcrunch} TechCrunch`
  }
  subtitle += ' for you.'
  return subtitle
}

export default function AIFrontiersArticles({ source, limit }: NewsletterProps) {
  const [searchParams] = useSearchParams();
  const date = searchParams.get('date');
  const [stories, setStories] = useState<Story[]>([])
  const [searchResults, setSearchResults] = useState<Story[]>([])
  const [searchQuery, setSearchQuery] = useState('')
  const [countBySource, setCountBySource] = useState<Record<string, number>>({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const setPlaylist = usePlayerStore(state => state.setPlaylist);

  useEffect(() => {
    const apiUrl = import.meta.env.VITE_BACKEND_API_URL;

    const fetchStories = async () => {
      try {
        setLoading(true)
        // Build the URL with query parameters
        const params = new URLSearchParams()
        // if (source) params.append('source', source)
        if (limit) params.append('limit', limit.toString())
        if (source) params.append('source', source)
        if (date) params.append('date', date)
        
        // Make sure to use the full URL path
        const response = await fetch(`${apiUrl}/news?${params.toString()}`, {
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
          },
        })

        // Log the response for debugging
        const contentType = response.headers.get('content-type')
        if (!contentType || !contentType.includes('application/json')) {
          // If not JSON, try to get the text content for debugging
          const text = await response.text()
          console.error('Invalid response type:', contentType, 'Response:', text)
          throw new Error('Invalid response type from server')
        }

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        
        const data = await response.json()
        if (!Array.isArray(data.stories)) {
          console.error('Unexpected data.stories format:', data)
          throw new Error('Invalid data.stories format received')
        }

        setStories(data.stories)
        setCountBySource(data.countBySource)
        setPlaylist(data.audioTracks)
      } catch (err) {
        console.error('Fetch error:', err)
        setError(err instanceof Error ? err.message : 'An error occurred while fetching stories')
      } finally {
        setLoading(false)
      }
    }
    fetchStories()
  }, [source, limit, setPlaylist])

  const handleSearchResults = (results: Story[], query: string) => {
    setSearchResults(results);
    setSearchQuery(query);
  };

  const content = loading ? (
    <div className="text-center py-8">Loading...</div>
  ) : error ? (
    <div className="text-center py-8 text-red-600 dark:text-red-400">{error}</div>
  ) : stories.length === 0 ? (
    <div className="text-center py-8 text-gray-600 dark:text-gray-300">No stories found</div>
  ) : (
    <div>
      <h1 className="text-4xl font-bold text-center text-blue-600 dark:text-blue-400 mb-2">
        {source ? `${source} News` : 'Latest AI News'}
      </h1>
      <p className="text-center text-gray-600 dark:text-gray-300">
        {date ? new Date(date).toLocaleDateString() : new Date().toLocaleDateString()}
      </p>
      <p className="text-center">
        {stories.length > 0 && getSubtitle(countBySource)}
      </p>
      <p className="text-center mb-8">
        {stories.length > 0 ? 'Please enjoy the gpt-4o summaries and AI-generated podcasts 🎧': ''}
      </p>
      
      {/* Search Box */}
      <div className="mb-8">
        <SearchBox 
          onResultsFound={handleSearchResults}
          className="mb-8"
        />
      </div>

      {/* Search Results or Original Stories */}
      {searchResults.length > 0 ? (
        <>
          <h2 className="text-2xl font-bold mb-4 dark:text-white text-center">Search Results</h2>
          {searchResults.map((story) => (
            <NewsletterCard key={story.story_id} story={story} />
          ))}
        </>
      ) : searchQuery ? (
        <div className="text-center py-8 text-gray-600 dark:text-gray-300">
          No matching stories found
        </div>
      ) : (
        stories.map((story) => (
          <NewsletterCard key={story.story_id} story={story} />
        ))
      )}
    </div>
  );

  return (
    <div className="relative z-0">
      {content}
    </div>
  );
}