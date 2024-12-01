import { Music2 } from 'lucide-react';
import { TrackList } from '../components/TrackList';
import { Player } from '../components/Player';
import { tracks } from '../data/tracks';

function AudioPlaylist() {
  return (
    <div className="min-h-screen bg-gray-900 dark:bg-gray-950 text-white">
      <div className="max-w-screen-lg mx-auto p-8">
        <div className="flex items-center space-x-4 mb-8">
          <Music2 className="w-8 h-8 text-green-500" />
          <h1 className="text-2xl font-bold text-white">Audio Player</h1>
        </div>

        <div className="mb-24">
          <h2 className="text-xl font-semibold mb-4 text-white">Featured Tracks</h2>
          <TrackList tracks={tracks} />
        </div>
      </div>
      <Player />
    </div>
  );
}

export default AudioPlaylist;