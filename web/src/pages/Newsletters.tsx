import React, { useEffect, useState } from 'react'
import { formatSummary } from '../lib/formatSummary'
import { useSearchParams } from 'react-router-dom';
import AudioButton from '../components/AudioButton';
// Types
interface Story {
  story_id: number
  title: string
  cover: string
  url: string
  hn_url?: string
  score?: number
  summary: string
  comments_summary?: string
  created_at: string
  source: string
  speech_url: string
  notebooklm_url: string
}

interface NewsletterProps {
  source?: string
  limit?: number
  date?: string
}

// Card components
const Card = ({ children, className = '' }: { children: React.ReactNode; className?: string }) => (
  <div className={`bg-white dark:bg-gray-800 shadow-md rounded-lg overflow-hidden ${className}`}>
    {children}
  </div>
)

const CardHeader = ({ children }: { children: React.ReactNode }) => (
  <div className="px-6 py-4 border-b border-gray-100 dark:border-gray-700">{children}</div>
)

const CardTitle = ({ children }: { children: React.ReactNode }) => (
  <h3 className="text-xl font-semibold text-gray-900 dark:text-white">{children}</h3>
)

const CardContent = ({ children }: { children: React.ReactNode }) => (
  <div className="px-6 py-4 prose dark:prose-invert max-w-none prose-headings:text-gray-900 dark:prose-headings:text-white prose-p:text-gray-700 dark:prose-p:text-gray-300 prose-a:text-blue-600 dark:prose-a:text-blue-400 prose-img:rounded-lg">
    {children}
  </div>
)

// Add this CSS class to your global styles or component
const summaryStyles = `
  .digest-list {
    list-style-type: disc;
    padding-left: 1.5rem;
    margin: 0.5rem 0;
  }
  .digest-list li {
    margin: 0.5rem 0;
    line-height: 1.5;
  }
  .digest-list li[style*="list-style: none"] {
    margin-left: -1.5rem;
  }
  .nested-list {
    list-style-type: circle;
    padding-left: 1.5rem;
    margin: 0.5rem 0;
  }
  .nested-list li {
    margin: 0.25rem 0;
  }
`

const getSourcePrefix = (source: string) => {
  const prefixes: Record<string, string> = {
    'hackernews': '[Hacker News] ',
    'techcrunch': '[TechCrunch] ',
    'arxiv': '[Arxiv] ',
    'latentspace': '[Latent Space]'
  };
  return prefixes[source.toLowerCase()] || '';
};

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
  const [countBySource, setCountBySource] = useState<Record<string, number>>({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

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
      } catch (err) {
        console.error('Fetch error:', err)
        setError(err instanceof Error ? err.message : 'An error occurred while fetching stories')
      } finally {
        setLoading(false)
      }
    }
    fetchStories()
  }, [source, limit])

  if (loading) {
    return <div className="text-center py-8">Loading...</div>
  }

  if (error) {
    return <div className="text-center py-8 text-red-600 dark:text-red-400">{error}</div>
  }

  return (
    <div className="relative z-0">
      {/* Add the styles to the component */}
      <style>{summaryStyles}</style>
      
      <h1 className="text-4xl font-bold text-center text-blue-600 dark:text-blue-400 mb-2">
        {source ? `${source} News` : 'Latest AI News'}
      </h1>
      <p className="text-center text-gray-600 dark:text-gray-300">{date ? new Date(date).toLocaleDateString() : new Date().toLocaleDateString()}</p>
      <p className="text-center">
        {stories.length > 0 && getSubtitle(countBySource)}
      </p>
      <p className="text-center mb-8">{stories.length > 0 ? 'Please enjoy the GPT-4o-mini summaries and AI-generated podcasts 🎧✨' : ''}</p>
      {stories.length === 0 ? (
        <p className="text-center text-gray-600 dark:text-gray-300">No stories found</p>
      ) : (
        stories.map((story) => (
          <Card key={story.story_id} className="mb-8">
            <CardHeader>
              <CardTitle>
                {getSourcePrefix(story.source)}{story.title}
              </CardTitle>
            </CardHeader>
            
            <div className="flex flex-col sm:flex-row items-start sm:items-center gap-2 px-6 py-2">
              <div className="flex flex-wrap items-center gap-2">
                <a href={story.url} className="text-blue-600 dark:text-blue-400 hover:underline cursor-pointer">
                  Original Article
                </a>
                {story.hn_url && (
                  <>
                    <span>•</span>
                    <a href={story.hn_url} className="text-blue-600 dark:text-blue-400 hover:underline cursor-pointer">
                      HN Discussion
                    </a>
                    <span>•</span>
                    <span className="text-gray-600 dark:text-gray-300">Score: {story.score}</span>
                  </>
                )}
                <span>•</span>
                <span className="text-gray-600 dark:text-gray-300">{new Date(story.created_at).toLocaleTimeString()}</span>
              </div>
              <div className="w-full sm:w-auto sm:ml-auto flex justify-start gap-2">
                {story.speech_url && (
                  <div>
                    <AudioButton 
                      speechUrl={story.speech_url} 
                      name="Audio" 
                      id={`${story.story_id}_audio`}
                      title={story.title}
                      type="Article audio"
                      createdAt={story.created_at}
                      cover={story.cover}
                    />
                  </div>
                )}
                {story.notebooklm_url && (
                  <div>
                    <AudioButton 
                      speechUrl={story.notebooklm_url} 
                      name="NotebookLM" 
                      id={`${story.story_id}_podcast`}
                      title={story.title}
                      type="AI-generated podcast"
                      createdAt={story.created_at}
                      cover={story.cover}
                    />
                  </div>
                )}
              </div>
            </div>

            <CardContent>
              <div className="space-y-6">
                {story.summary && (
                  <div className="text-gray-700 dark:text-gray-300">
                    <h3 className="font-semibold text-lg mb-3">Article Summary</h3>
                    <div
                      dangerouslySetInnerHTML={{ __html: formatSummary(story.summary) }} 
                    />
                  </div>
                )}
                
                {story.comments_summary && (
                  <div className="text-gray-700 dark:text-gray-300">
                    <h3 className="font-semibold text-lg mb-3">Discussion Highlights</h3>
                    <div 
                      dangerouslySetInnerHTML={{ __html: formatSummary(story.comments_summary) }} 
                    />
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        ))
      )}
    </div>
  )
}