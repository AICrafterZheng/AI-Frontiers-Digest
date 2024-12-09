import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';
import { Track } from '../types/types';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatTime(seconds: number): string {
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = Math.floor(seconds % 60);
  return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
}

export function getSourcePrefix(source: string) {
  if (!source) {
    return '';
  }
  const prefixes: Record<string, string> = {
    'hackernews': '[Hacker News] ',
    'techcrunch': '[TechCrunch] ',
    'arxiv': '[Arxiv] ',
    'latentspace': '[Latent Space]'
  };
  return prefixes[source.toLowerCase()] || '';
};

export function getTrackCover(source: string): string {
  const defaultCover = "https://dyesbzillwyznubkjgbp.supabase.co/storage/v1/object/public/images/ai.svg";
  if (!source) {
    return defaultCover;
  }
  if (source.toLowerCase() === "techcrunch") {
    return "https://dyesbzillwyznubkjgbp.supabase.co/storage/v1/object/public/images/tc.png";
  } else if (source.toLowerCase() === "hackernews") {
    return "https://dyesbzillwyznubkjgbp.supabase.co/storage/v1/object/public/images/yc.png";
  } else {
    return defaultCover;
  }
}

export function constructResult(data: any) {
    // Count by source - only count if source exists and is not empty
    const countBySource = data?.reduce((acc: any, story: any) => {
      if (story?.source) {
        const sourceKey = story.source.toLowerCase();
        acc[sourceKey] = (acc[sourceKey] || 0) + 1;
      }
      return acc;
    }, {});

    // add cover to each story
    const stories = data?.map((story: any) => {
      if (story?.source) {
        story.cover = getTrackCover(story.source);
      } else {
        story.cover = ''; // or provide a default cover
      }
      return story;
    });

    // Initialize empty tracks array
    const tracks: Track[] = [];
    
    // Only process audio tracks if there are stories with audio URLs
    if (data && data.length > 0) {
      data.forEach((story: any) => {
        const cover = story?.source ? getTrackCover(story.source) : ''; // default empty string if no source
        // Push speech URL track
        if (story?.speech_url) {
          tracks.push({
            id: story.story_id?.toString() + "_audio",
            cover: cover,
            title: story.title || '',
            type: "Article audio",
            audioUrl: story.speech_url,
            createdAt: story.created_at
          });
        }
        
        // Push notebook URL track
        if (story?.notebooklm_url) {
          tracks.push({
            id: story.story_id?.toString() + "_podcast",
            cover: cover,
            title: story.title || '',
            type: "AI-generated podcast",
            audioUrl: story.notebooklm_url,
            createdAt: story.created_at,
          });
        }
      });
    }
    // Return the constructed result
    return {stories: stories || [], audioTracks: tracks || [], countBySource: countBySource}
}