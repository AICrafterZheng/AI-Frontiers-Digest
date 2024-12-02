import { createClient } from '@supabase/supabase-js'
import { create } from 'zustand';

export async function onRequest(context: any) {
  const supabase = createClient(
    context.env.SUPABASE_URL,
    context.env.SUPABASE_ANON_KEY
  );

  try {
    const { data: stories, error } = await supabase
      .from(context.env.SUPABASE_TABLE_STORIES)
      .select('story_id, title, speech_url, notebooklm_url, created_at')
      .order('created_at', { ascending: false })
      .not('speech_url', 'is', null)
      .not('notebooklm_url', 'is', null);

    if (error) {
      throw error;
    }

    const tracks = stories.map((story: any, index: number) => ({
      id: story.story_id.toString(),
      title: story.title,
      artist: 'AI Frontiers Digest',
      cover: 'https://images.unsplash.com/photo-1677442136019-21780ecad995', // AI/tech themed image
      audioUrl: story.speech_url,
      notebookUrl: story.notebooklm_url,
      createdAt: story.created_at
    }));

    return new Response(JSON.stringify({ tracks }), {
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
    });
  } catch (error) {
    console.error('Error fetching audio tracks:', error);
    return new Response(JSON.stringify({ error: 'Failed to fetch audio tracks' }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
    });
  }
}
