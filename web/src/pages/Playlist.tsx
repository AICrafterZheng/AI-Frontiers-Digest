import { Music2 } from 'lucide-react';
import { TrackList } from '../components/TrackList';
import { useEffect, useState } from 'react';
import { Track } from '../types/audio';
import { fetchTracks } from '../services/audioService';
import { usePlayerStore } from '../store/usePlayerStore';

function AudioPlaylist() {
  const [tracks, setTracks] = useState<Track[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const setPlaylist = usePlayerStore(state => state.setPlaylist);

  useEffect(() => {
    async function loadTracks() {
      try {
        const fetchedTracks = await fetchTracks();
        setTracks(fetchedTracks);
        setPlaylist(fetchedTracks); // Set playlist in store
      } catch (err) {
        setError('Failed to load audio tracks');
        console.error('Error loading tracks:', err);
      } finally {
        setLoading(false);
      }
    }
    loadTracks();
  }, [setPlaylist]);

  const content = loading ? (
    <div className="text-center text-gray-600 dark:text-gray-400">Loading tracks...</div>
  ) : error ? (
    <div className="text-center text-red-600 dark:text-red-400">{error}</div>
  ) : tracks.length === 0 ? (
    <div className="text-center text-gray-600 dark:text-gray-400">No audio tracks available</div>
  ) : (
    <TrackList tracks={tracks} />
  );

  return (
    <div className="container mx-auto px-4">
      <div className="flex items-center gap-2 mb-6">
        <Music2 className="w-6 h-6 text-gray-900 dark:text-white" />
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Audio Playlist</h1>
      </div>
      
      {/* Mobile view */}
      <div className="sm:hidden">
        {content}
      </div>

      {/* Desktop view */}
      <div className="hidden sm:block">
        {content}
      </div>
    </div>
  );
}

export default AudioPlaylist;