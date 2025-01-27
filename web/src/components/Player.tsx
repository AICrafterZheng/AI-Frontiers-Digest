import React, { useEffect, useRef, useState } from 'react';
import { Play, Pause, SkipBack, SkipForward, X } from 'lucide-react';
import { usePlayerStore } from '../store/usePlayerStore';
import { formatTime } from '../lib/utils';

export function Player() {
  const {
    currentTrack,
    isPlaying,
    isVisible,
    setIsPlaying,
    playNext,
    playPrevious,
    close
  } = usePlayerStore();
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const audioRef = useRef<HTMLAudioElement>(null);

  useEffect(() => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.play();
      } else {
        audioRef.current.pause();
      }
    }
  }, [isPlaying, currentTrack]);

  const handleTimeUpdate = () => {
    if (audioRef.current) {
      setCurrentTime(audioRef.current.currentTime);
      setDuration(audioRef.current.duration);
    }
  };

  const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (audioRef.current) {
      const time = Number(e.target.value);
      audioRef.current.currentTime = time;
      setCurrentTime(time);
    }
  };

  const handleEnded = () => {
    setIsPlaying(false);
    playNext();
  };

  if (!currentTrack || !isVisible) return null;

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-gray-900 dark:bg-black border-t border-gray-800 dark:border-gray-700 p-4">
      <button
        onClick={close}
        className="absolute top-2 right-4 text-gray-400 hover:text-white transition-colors"
        aria-label="Close player"
      >
        <X className="w-5 h-5" />
      </button>
      
      <div className="max-w-screen-lg mx-auto flex flex-col sm:flex-row items-center gap-4">
        {/* Title and cover section - flexible width */}
        <div className="flex items-center gap-4 w-full sm:flex-1">
          <img
            src={currentTrack.cover}
            alt={currentTrack.title}
            className="w-8 h-8 sm:w-16 sm:h-16 rounded object-cover"
          />
          
          <div className="flex-1 min-w-0">
            <h3 className="font-semibold text-white truncate max-w-[300px] sm:max-w-[800px]">{currentTrack.title}</h3>
            <p className="text-sm text-gray-400 truncate max-w-[300px] sm:max-w-[800px]">{currentTrack.type}</p>
          </div>
        </div>

        {/* Playback controls section - fixed width */}
        <div className="w-full sm:w-[220px] flex flex-col items-center shrink-0">
          <div className="w-full flex items-center justify-center space-x-4 mb-2">
            <button
              onClick={playPrevious}
              className="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
            >
              <SkipBack className="w-5 h-5 text-gray-400 cursor-pointer hover:text-white transition-colors" />
            </button>
            <button
              onClick={() => setIsPlaying(!isPlaying)}
              className="p-2 rounded-full bg-white dark:bg-black hover:bg-gray-200 dark:hover:bg-gray-900 transition-colors"
            >
              {isPlaying ? (
                <Pause className="w-6 h-6 text-black dark:text-white" />
              ) : (
                <Play className="w-6 h-6 text-black dark:text-white" />
              )}
            </button>
            <button
              onClick={playNext}
              className="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
            >
              <SkipForward className="w-5 h-5 text-gray-400 cursor-pointer hover:text-white transition-colors" />
            </button>
          </div>

          <div className="w-full flex items-center gap-3 text-sm text-gray-400">
            <span className="w-12 text-right">{formatTime(currentTime)}</span>
            <input
              type="range"
              min="0"
              max={duration || 0}
              value={currentTime}
              onChange={handleSeek}
              className="flex-1 h-1 bg-gray-700 rounded-lg appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-3 [&::-webkit-slider-thumb]:h-3 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-white"
            />
            <span className="w-12">{formatTime(duration)}</span>
          </div>
        </div>
      </div>

      <audio
        ref={audioRef}
        src={currentTrack.audioUrl}
        onTimeUpdate={handleTimeUpdate}
        onEnded={handleEnded}
      />
    </div>
  );
}