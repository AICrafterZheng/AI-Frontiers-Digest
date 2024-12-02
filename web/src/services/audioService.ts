import { Track } from '../types/types';

export async function fetchTracks(): Promise<Track[]> {
  try {
    const apiUrl = import.meta.env.VITE_BACKEND_API_URL;
    const response = await fetch(`${apiUrl}/audio`);
    if (!response.ok) {
      throw new Error('Failed to fetch tracks');
    }
    const data = await response.json();
    return data.tracks;
  } catch (error) {
    console.error('Error fetching tracks:', error);
    return [];
  }
}
