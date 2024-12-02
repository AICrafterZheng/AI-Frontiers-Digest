import AudioButton from "./AudioButton";
import { getSourcePrefix } from "../lib/utils";
import { formatSummary } from '../lib/formatSummary'
import {  NewsletterCardProps } from "../types/types";


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


export function NewsletterCard({ story }: NewsletterCardProps) {
  return (
    <Card className="mb-8">
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
  );
}
