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
          className={`flex items-center space-x-4 p-4 rounded-lg hover:bg-white/5 cursor-pointer ${
            currentTrack?.id === track.id ? 'bg-white/10' : ''
          }`}
          onClick={() => handlePlay(track)}
        >
          <img
            src={track.cover}
            alt={track.title}
            className="w-12 h-12 rounded object-cover"
          />
          <div className="flex-1">
            <h3 className="font-semibold text-white">{track.title}</h3>
            <p className="text-sm text-gray-400">{track.artist}</p>
          </div>
          <Play className="w-5 h-5 text-gray-400" />
        </div>
      ))}
    </div>
  );
}