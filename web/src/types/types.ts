export interface Track {
  id: string;
  title: string;
  type: string;
  cover: string;
  audioUrl: string;
  createdAt: string;
}

export interface Story {
  id: number;
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

export interface NewsletterCardProps {
  story: Story;
}

export interface NewsletterProps {
  source?: string
  limit?: number
  date?: string
}