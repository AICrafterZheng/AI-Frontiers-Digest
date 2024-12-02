import React, { useState, useEffect } from 'react';
import { Volume2, Volume1 } from 'lucide-react';
import { useAudioContext } from '../store/useAudioContext';

interface AudioButtonProps {
  speechUrl: string;
  name: string;
  className?: string;
}

export default function AudioButton({ speechUrl, name, className = '' }: AudioButtonProps) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [duration, setDuration] = useState<number | null>(null);
  const audioRef = React.useRef<HTMLAudioElement>(null);
  const { currentlyPlayingUrl, setCurrentlyPlaying } = useAudioContext();

  useEffect(() => {
    // Create temporary audio element to get duration
    const audio = new Audio(speechUrl);
    audio.addEventListener('loadedmetadata', () => {
      setDuration(audio.duration);
    });
  }, [speechUrl]);

  // Stop playing if another audio starts
  useEffect(() => {
    if (currentlyPlayingUrl && currentlyPlayingUrl !== speechUrl && isPlaying) {
      if (audioRef.current) {
        audioRef.current.pause();
        setIsPlaying(false);
      }
    }
  }, [currentlyPlayingUrl, speechUrl, isPlaying]);

  // Format duration to MM:SS
  const formatTime = (time: number): string => {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  const togglePlay = () => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause();
        setCurrentlyPlaying(null);
      } else {
        // Stop any currently playing audio
        if (currentlyPlayingUrl && currentlyPlayingUrl !== speechUrl) {
          const currentAudio = document.querySelector(`audio[src="${currentlyPlayingUrl}"]`) as HTMLAudioElement;
          if (currentAudio) {
            currentAudio.pause();
          }
        }
        audioRef.current.play();
        setCurrentlyPlaying(speechUrl);
      }
      setIsPlaying(!isPlaying);
    }
  };

  return (
    <div className={`flex items-center gap-2 ${className}`}>
      <button
        onClick={togglePlay}
        className="flex items-center gap-2 px-3 py-1.5 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
      >
        {isPlaying ? <Volume2 className="w-4 h-4" /> : <Volume1 className="w-4 h-4" />}
        <span>{name}</span>
        {duration && <span className="text-xs text-gray-500">({formatTime(duration)})</span>}
      </button>

      <audio
        ref={audioRef}
        src={speechUrl}
        onEnded={() => {
          setIsPlaying(false);
          setCurrentlyPlaying(null);
        }}
      />
    </div>
  );
}