import { useEffect, useState } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom';
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
  const navigate = useNavigate();
  const date = searchParams.get('date')
  const [stories, setStories] = useState<Story[]>([])
  const [searchResults, setSearchResults] = useState<Story[]>([])
  const [searchQuery, setSearchQuery] = useState('')
  const [countBySource, setCountBySource] = useState<Record<string, number>>({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const setPlaylist = usePlayerStore(state => state.setPlaylist);

  const handlePrevDay = () => {
    const currentDate = date ? new Date(date) : new Date().toLocaleDateString();
    const prevDate = new Date(currentDate);
    prevDate.setDate(prevDate.getDate() + 1);
    const today = new Date();
    
    // Prevent navigating to future dates
    if (prevDate > today) {
      console.log('Cannot navigate to future date');
      return;
    }
    
    const formattedDate = prevDate.toISOString().split('T')[0];
    console.log('Navigating to previous day:', formattedDate);
    navigate(`/articles?date=${formattedDate}`);
  };

  const handleNextDay = () => {
    const currentDate = date ? new Date(date) : new Date().toLocaleDateString();
    const nextDate = new Date(currentDate);
    nextDate.setDate(nextDate.getDate() - 1);
    const formattedDate = nextDate.toISOString().split('T')[0];
    console.log('Navigating to next day:', formattedDate);
    navigate(`/articles?date=${formattedDate}`);
  };

  useEffect(() => {
    console.log('Current date param:', date);
    const apiUrl = import.meta.env.VITE_BACKEND_API_URL;

    const fetchStories = async () => {
      try {
        setLoading(true)
        // Build the URL with query parameters
        const params = new URLSearchParams()
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
  }, [source, limit, date, setPlaylist])

  const handleSearchResults = (results: Story[], query: string) => {
    setSearchResults(results);
    setSearchQuery(query);
  };

  const content = loading ? (
    <div className="text-center py-8">Loading...</div>
  ) : error ? (
    <div className="text-center py-8 text-red-600 dark:text-red-400">{error}</div>
  ) : stories.length === 0 ? (
    <div className="text-center py-8 text-gray-600 dark:text-gray-300">No stories found on the selected date, please try a different date.</div>
  ) : (
    <div>
      <h1 className="text-4xl font-bold text-center bg-gradient-to-r from-blue-600 via-purple-600 to-blue-600 dark:from-blue-400 dark:via-purple-400 dark:to-blue-400 bg-clip-text text-transparent animate-gradient mb-2">
        {source ? `${source} News` : 'Latest AI News'}
      </h1>
      <p className="text-center text-gray-600 dark:text-gray-300">        
        {/* check if current time is before 12pm don't add T12:00:00Z */}
        {date ? (new Date().getHours() < 12 ? new Date(date).toLocaleDateString() : new Date(`${date}T12:00:00Z`).toLocaleDateString()) : new Date().toLocaleDateString()}
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
      
      {/* Navigation Buttons */}
      <div className="flex justify-center gap-4 my-8">
        <button
          onClick={handlePrevDay}
          className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          disabled={new Date(date) >= new Date()}
        >
          ← Pre
        </button>
        <button
          onClick={handleNextDay}
          className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
        >
          Next →
        </button>
      </div>
    </div>
  );
}