import { useState, useEffect } from 'react';
import { Volume2, Volume1 } from 'lucide-react';
import { usePlayerStore } from '../store/usePlayerStore';
interface AudioButtonProps {
  speechUrl: string;
  name: string;
  className?: string;
  title: string;
  type: string;
  createdAt: string;
  id: string;
  cover: string;
}

export default function AudioButton({ 
  speechUrl, 
  name, 
  className = '',
  title,
  type,
  createdAt,
  id,
  cover
}: AudioButtonProps) {
  const [duration, setDuration] = useState<number | null>(null);
  const { currentTrack, isPlaying, setTrack, setIsPlaying } = usePlayerStore();
  const isThisPlaying = isPlaying && currentTrack?.audioUrl === speechUrl;

  useEffect(() => {
    // Create temporary audio element to get duration
    const audio = new Audio(speechUrl);
    audio.addEventListener('loadedmetadata', () => {
      setDuration(audio.duration);
    });
  }, [speechUrl]);

  // Format duration to MM:SS
  const formatTime = (time: number): string => {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  const togglePlay = () => {
    const track = {
      id,
      title,
      type,
      audioUrl: speechUrl,
      createdAt,
      cover
    };

    if (isThisPlaying) {
      setIsPlaying(false);
    } else {
      setTrack(track);
      setIsPlaying(true);
    }
  };

  return (
    <div className={`flex items-center gap-2 ${className}`}>
      <button
        onClick={togglePlay}
        className="flex items-center gap-2 px-3 py-1.5 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-black rounded-lg hover:bg-gray-200 dark:hover:bg-gray-900 transition-colors"
      >
        {isThisPlaying ? <Volume2 className="w-4 h-4" /> : <Volume1 className="w-4 h-4" />}
        <span>{name}</span>
        {duration && <span className="text-xs text-gray-500">({formatTime(duration)})</span>}
      </button>
    </div>
  );
}