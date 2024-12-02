import { create } from 'zustand';
import { Track } from '../types/audio';

interface PlayerState {
  currentTrack: Track | null;
  playlist: Track[];
  isPlaying: boolean;
  volume: number;
  setTrack: (track: Track) => void;
  setPlaylist: (playlist: Track[]) => void;
  setIsPlaying: (isPlaying: boolean) => void;
  setVolume: (volume: number) => void;
  playNext: () => void;
}

export const usePlayerStore = create<PlayerState>((set, get) => ({
  currentTrack: null,
  playlist: [],
  isPlaying: false,
  volume: 1,
  setTrack: (track) => set({ currentTrack: track }),
  setPlaylist: (playlist) => set({ playlist }),
  setIsPlaying: (isPlaying) => set({ isPlaying }),
  setVolume: (volume) => set({ volume }),
  playNext: () => {
    const { currentTrack, playlist } = get();
    if (!currentTrack || playlist.length === 0) return;
    
    const currentIndex = playlist.findIndex(track => track.id === currentTrack.id);
    if (currentIndex === -1 || currentIndex === playlist.length - 1) {
      // If last track or track not found, stop playing
      set({ isPlaying: false });
      return;
    }
    
    // Play next track
    const nextTrack = playlist[currentIndex + 1];
    set({ currentTrack: nextTrack, isPlaying: true });
  },
}));