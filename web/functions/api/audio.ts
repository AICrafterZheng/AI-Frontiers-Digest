import { createClient } from '@supabase/supabase-js'
import { Track } from '../../src/types/types';

export async function onRequest(context: any) {
  const supabase = createClient(
    context.env.SUPABASE_URL,
    context.env.SUPABASE_ANON_KEY
  );

  try {
    const { data: stories, error } = await supabase
      .from(context.env.SUPABASE_TABLE_STORIES)
      .select('story_id, title, speech_url, notebooklm_url, created_at, source')
      .order('created_at', { ascending: false })
      .not('speech_url', 'is', null)
      .not('notebooklm_url', 'is', null);

    if (error) {
      throw error;
    }
    
    
    // Define tracks array with type
    const tracks: Track[] = [];
    stories.forEach((story: any) => {
      // Push speech URL track
      let cover;
      if (story.source.toLowerCase()   === "techcrunch") {
        cover = "https://dyesbzillwyznubkjgbp.supabase.co/storage/v1/object/public/images/tc.png";
      } else if (story.source.toLowerCase() === "hackernews") {
        cover = "https://dyesbzillwyznubkjgbp.supabase.co/storage/v1/object/public/images/yc.png";
      } else {
        cover = "https://dyesbzillwyznubkjgbp.supabase.co/storage/v1/object/public/images/ai.svg";
      }
      if (story.speech_url) {
        tracks.push({
          id: story.story_id.toString() + "_audio",
          cover: cover,
          title: story.title,
          type: "Article audio",
          audioUrl: story.speech_url,
          createdAt: story.created_at
        });
      }
      
      // Push notebook URL track
      if (story.notebooklm_url) {
        tracks.push({
          id: story.story_id.toString() + "_podcast",
          cover: cover,
          title: story.title,
          type: "AI-generated podcast",
          audioUrl: story.notebooklm_url,
          createdAt: story.created_at,
        });
      }
    });

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
