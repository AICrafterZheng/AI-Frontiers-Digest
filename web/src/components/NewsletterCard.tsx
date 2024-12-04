import AudioButton from "./AudioButton";
import { getSourcePrefix } from "../lib/utils";
import { formatSummary } from '../lib/formatSummary'
import { NewsletterCardProps } from "../types/types";
import '../styles/summary.css';
import { useState } from 'react';

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
  <div className="px-6 py-4 prose dark:prose-invert max-w-none prose-headings:text-gray-900 dark:prose-headings:text-white prose-p:text-gray-700 dark:prose-p:text-gray-300 prose-a:text-blue-600 dark:prose-a:text-blue-400 prose-img:rounded-lg prose-ul:list-disc prose-ul:pl-6">
    {children}
  </div>
)


export function NewsletterCard({ story }: NewsletterCardProps) {
  const [showCopied, setShowCopied] = useState(false);

  const handleShare = async () => {
    const shareUrl = `${window.location.origin}/news/${story.id}`;
    try {
      await navigator.clipboard.writeText(shareUrl);
      setShowCopied(true);
      setTimeout(() => setShowCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  return (
    <Card className="mb-8">
      <CardHeader>
        <div className="flex justify-between items-center">
          <CardTitle>
            {getSourcePrefix(story.source)}{story.title}
          </CardTitle>
          <button
            onClick={handleShare}
            className="flex items-center gap-1 text-gray-500 hover:text-blue-600 dark:text-gray-400 dark:hover:text-blue-400 transition-colors"
            title="Share article"
          >
            {showCopied ? (
              <span className="text-sm">Copied!</span>
            ) : (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path d="M15 8a3 3 0 10-2.977-2.63l-4.94 2.47a3 3 0 100 4.319l4.94 2.47a3 3 0 10.895-1.789l-4.94-2.47a3.027 3.027 0 000-.74l4.94-2.47C13.456 7.68 14.19 8 15 8z" />
              </svg>
            )}
          </button>
        </div>
      </CardHeader>
      
      <div className="flex flex-col sm:flex-row items-start sm:items-center gap-2 px-6 py-2">
        <div className="flex flex-wrap items-center gap-2">
          <a 
            href={story.url} 
            className="text-blue-600 dark:text-blue-400 hover:underline cursor-pointer"
            target="_blank"
            rel="noopener noreferrer"
          >
            Original Article
          </a>
          {story.hn_url && (
            <>
              <span>•</span>
              <a 
                href={story.hn_url} 
                className="text-blue-600 dark:text-blue-400 hover:underline cursor-pointer"
                target="_blank"
                rel="noopener noreferrer"
              >
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
  );
}
