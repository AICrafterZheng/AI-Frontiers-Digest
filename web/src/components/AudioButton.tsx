import React, { useState, useEffect } from 'react';

interface AudioButtonProps {
  speechUrl: string;
  name: string;
}

export default function AudioButton({ speechUrl, name }: AudioButtonProps) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [duration, setDuration] = useState<number | null>(null);
  const audioRef = React.useRef<HTMLAudioElement>(null);

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
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause();
      } else {
        audioRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  return (
    <div className="flex items-center gap-2">
      <button
        onClick={togglePlay}
        className="flex items-center gap-2 px-3 py-1 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
      >
        {isPlaying ? (
          <>
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 9v6m4-6v6" />
            </svg>
            Pause
          </>
        ) : (
          <>
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {name} {duration && `(${formatTime(duration)})`}
          </>
        )}
      </button>
      <audio
        ref={audioRef}
        src={speechUrl}
        onEnded={() => setIsPlaying(false)}
      />
    </div>
  );
}; 