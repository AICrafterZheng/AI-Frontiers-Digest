import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatTime(seconds: number): string {
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = Math.floor(seconds % 60);
  return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
}

export function getSourcePrefix(source: string) {
  const prefixes: Record<string, string> = {
    'hackernews': '[Hacker News] ',
    'techcrunch': '[TechCrunch] ',
    'arxiv': '[Arxiv] ',
    'latentspace': '[Latent Space]'
  };
  return prefixes[source.toLowerCase()] || '';
};

export function getTrackCover(source: string): string {
  if (source.toLowerCase() === "techcrunch") {
    return "https://dyesbzillwyznubkjgbp.supabase.co/storage/v1/object/public/images/tc.png";
  } else if (source.toLowerCase() === "hackernews") {
    return "https://dyesbzillwyznubkjgbp.supabase.co/storage/v1/object/public/images/yc.png";
  } else {
    return "https://dyesbzillwyznubkjgbp.supabase.co/storage/v1/object/public/images/ai.svg";
  }
}