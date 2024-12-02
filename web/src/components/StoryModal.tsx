import { X } from 'lucide-react';
import { NewsletterCard } from './NewsletterCard';

interface Story {
  story_id: number;
  title: string;
  url: string;
  hn_url?: string;
  score?: number;
  created_at: string;
  summary?: string;
  comments_summary?: string;
  speech_url?: string;
  notebooklm_url?: string;
  source: string;
  cover: string;
}

interface StoryModalProps {
  story: Story | null;
  onClose: () => void;
}

export function StoryModal({ story, onClose }: StoryModalProps) {
  if (!story) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className="bg-white dark:bg-gray-900 rounded-lg w-full max-w-4xl max-h-[90vh] overflow-y-auto relative">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
        >
          <X className="w-6 h-6" />
        </button>
        <div className="p-4">
          <NewsletterCard story={story} />
        </div>
      </div>
    </div>
  );
}
