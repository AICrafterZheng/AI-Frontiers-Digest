import React from 'react';
import { Play } from 'lucide-react';
import { Track } from '../types/audio';
import { usePlayerStore } from '../store/usePlayerStore';

interface TrackListProps {
  tracks: Track[];
}

export function TrackList({ tracks }: TrackListProps) {
  const { setTrack, setIsPlaying, currentTrack } = usePlayerStore();

  const handlePlay = (track: Track) => {
    setTrack(track);
    setIsPlaying(true);
  };

  return (
    <div className="space-y-4">
      {tracks.map((track) => (
        <div
          key={track.id}
          className={`flex items-center space-x-4 p-4 rounded-lg bg-gray-50 dark:bg-gray-700/50 hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer transition-colors ${
            currentTrack?.id === track.id ? 'bg-gray-100 dark:bg-gray-700' : ''
          }`}
          onClick={() => handlePlay(track)}
        >
          <img
            src={track.cover}
            alt={track.title}
            className="w-12 h-12 rounded object-cover"
          />
          <div className="flex-1 min-w-0">
            <h3 className="text-base font-medium text-gray-900 dark:text-white truncate">
              {track.title}
            </h3>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              {track.artist}
            </p>
          </div>
          <Play className="w-6 h-6 text-gray-400 dark:text-gray-500" />
        </div>
      ))}
    </div>
  );
}