import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { NewsletterCard } from '../components/NewsletterCard';
import { Track, Story } from '../types/types';

const Newsletter: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [story, setStory] = useState<Story | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const apiUrl = import.meta.env.VITE_BACKEND_API_URL;
    const fetchStory = async () => {
      try {
        const response = await fetch(`${apiUrl}/news?id=${id}`);
        if (!response.ok) {
          if (response.status === 404) {
            navigate('/404');
            return;
          }
          throw new Error('Failed to fetch story');
        }
        const data = await response.json();
        const stories = data.stories || [];
        if (!stories || stories.length === 0) {
          // Navigate to 404 page
          navigate('/404');
          return;
        }
        setStory(stories[0]);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchStory();
    }
  }, [id, navigate]);

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900 dark:border-white"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <p className="text-red-500">{error}</p>
      </div>
    );
  }

  if (!story) {
    return null;
  }

  // Convert story to tracks for audio player
  const tracks: Track[] = [];
  if (story.speech_url) {
    tracks.push({
      id: story.story_id.toString() + "_audio",
      cover: story.cover || "",
      title: story.title,
      type: "Article audio",
      audioUrl: story.speech_url,
      createdAt: story.created_at
    });
  }
  if (story.notebooklm_url) {
    tracks.push({
      id: story.story_id.toString() + "_podcast",
      cover: story.cover || "",
      title: story.title,
      type: "AI-generated podcast",
      audioUrl: story.notebooklm_url,
      createdAt: story.created_at,
    });
  }

  return (
    <div className="max-w-4xl mx-auto px-4">
      <NewsletterCard
        story={story}
      />
    </div>
  );
};

export default Newsletter;
