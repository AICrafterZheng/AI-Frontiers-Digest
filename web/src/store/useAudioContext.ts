import { create } from 'zustand';

interface AudioContextState {
  currentlyPlayingUrl: string | null;
  setCurrentlyPlaying: (url: string | null) => void;
}

export const useAudioContext = create<AudioContextState>((set) => ({
  currentlyPlayingUrl: null,
  setCurrentlyPlaying: (url) => set({ currentlyPlayingUrl: url }),
}));
