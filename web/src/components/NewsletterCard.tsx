import AudioButton from "./AudioButton";
import { getSourcePrefix } from "../lib/utils";
import { formatSummary } from '../lib/formatSummary'
import { NewsletterCardProps } from "../types/types";
import '../styles/summary.css';
import { useState } from 'react';

// Card components
const Card = ({ children, className = '' }: { children: React.ReactNode; className?: string }) => (
  <div className={`bg-white dark:bg-black shadow-md rounded-lg overflow-hidden ${className}`}>
    {children}
  </div>
)

const CardHeader = ({ children, onClick, isExpanded }: { children: React.ReactNode; onClick?: () => void; isExpanded?: boolean }) => (
  <div 
    className={`px-6 py-4 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-900 transition-colors ${
      isExpanded ? 'border-b border-gray-200 dark:border-gray-800' : 'border border-gray-200 dark:border-gray-800 rounded-lg'
    }`}
    onClick={onClick}
  >
    {children}
  </div>
)

const CardTitle = ({ children }: { children: React.ReactNode }) => (
  <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-300">{children}</h3>
)

const CardContent = ({ children }: { children: React.ReactNode }) => (
  <div className="px-6 py-4 prose dark:prose-invert max-w-none prose-headings:text-gray-900 dark:prose-headings:text-gray-300 prose-p:text-gray-700 dark:prose-p:text-gray-400 prose-a:text-blue-600 dark:prose-a:text-blue-400 prose-img:rounded-lg prose-ul:list-disc prose-ul:pl-6">
    {children}
  </div>
)

export function NewsletterCard({ story, expanded = false }: NewsletterCardProps) {
  const [showCopied, setShowCopied] = useState(false);
  const [isExpanded, setIsExpanded] = useState(expanded);

  const handleCopyLink = (e: React.MouseEvent) => {
    e.stopPropagation(); // Prevent header click from triggering
    const shareUrl = `${window.location.origin}/news/${story.id}`;
    const tempInput = document.createElement('input');
    tempInput.value = shareUrl;
    document.body.appendChild(tempInput);
    tempInput.select();
    document.execCommand('copy');
    document.body.removeChild(tempInput);
    setShowCopied(true);
    setTimeout(() => setShowCopied(false), 500);
  };

  return (
    <Card className="mb-8 newsletter-card">
      <div className={`${isExpanded ? 'border border-gray-200 dark:border-gray-800 rounded-lg' : ''}`}>
        <CardHeader onClick={() => setIsExpanded(!isExpanded)} isExpanded={isExpanded}>
          <div className="flex justify-between items-center">
            <CardTitle>
              <div className="flex items-center">
                <svg 
                  className={`w-5 h-5 mr-2 transform transition-transform ${isExpanded ? 'rotate-90' : ''}`} 
                  fill="currentColor" 
                  viewBox="0 0 20 20"
                >
                  <path 
                    fillRule="evenodd" 
                    d="M7.293 4.707a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L10.586 10 7.293 6.707a1 1 0 010-1.414z" 
                    clipRule="evenodd" 
                  />
                </svg>
                {getSourcePrefix(story.source)}{story.title}
              </div>
            </CardTitle>
            <button
              onClick={handleCopyLink}
              className="ml-2 p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 transition-colors"
              title="Copy link"
            >
            {showCopied ? (
              <svg viewBox="0 0 24 24" className="h-5 w-5 text-blue-400" fill="currentColor">
                <g>
                  <path d="M12 2.59l5.7 5.7-1.41 1.41L13 6.41V16h-2V6.41l-3.3 3.3-1.41-1.41L12 2.59zM21 15l-.02 3.51c0 1.38-1.12 2.49-2.5 2.49H5.5C4.11 21 3 19.88 3 18.5V15h2v3.5c0 .28.22.5.5.5h12.98c.28 0 .5-.22.5-.5L19 15h2z" />
                </g>
              </svg>
            ) : (
              <svg viewBox="0 0 24 24" className="h-5 w-5" fill="currentColor">
                <g>
                  <path d="M12 2.59l5.7 5.7-1.41 1.41L13 6.41V16h-2V6.41l-3.3 3.3-1.41-1.41L12 2.59zM21 15l-.02 3.51c0 1.38-1.12 2.49-2.5 2.49H5.5C4.11 21 3 19.88 3 18.5V15h2v3.5c0 .28.22.5.5.5h12.98c.28 0 .5-.22.5-.5L19 15h2z" />
                </g>
              </svg>
            )}
            </button>
          </div>
        </CardHeader>
        
        {isExpanded && (
          <>
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
                    <span className="text-gray-600 dark:text-gray-400">Score: {story.score}</span>
                  </>
                )}
                <span className="text-gray-600 dark:text-gray-400"><span>• </span>{new Date(story.created_at).toLocaleString()}</span>
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
                      name="Podcast" 
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
                  <div className="text-gray-700 dark:text-gray-400">
                    <h3 className="font-semibold text-lg mb-3">Article Summary</h3>
                    <div
                      dangerouslySetInnerHTML={{ __html: formatSummary(story.summary) }} 
                    />
                  </div>
                )}
                
                {story.comments_summary && (
                  <div className="text-gray-700 dark:text-gray-400">
                    <h3 className="font-semibold text-lg mb-3">Discussion Highlights</h3>
                    <div 
                      dangerouslySetInnerHTML={{ __html: formatSummary(story.comments_summary) }} 
                    />
                  </div>
                )}
              </div>
            </CardContent>
          </>
        )}
      </div>
    </Card>
  );
}
