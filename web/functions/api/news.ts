import { createClient } from '@supabase/supabase-js'
import { Track } from '../../src/types/types';
import { getTrackCover } from '../../src/lib/utils';

async function getLastRecordDate(supabase: any, tableName: string): Promise<string | null> {
  try {
    const { data, error } = await supabase
      .from(tableName)
      .select('created_at')
      .order('created_at', { ascending: false })
      .limit(1);

    if (error) {
      console.error('Error fetching last record:', error);
      return null;
    }

    return data?.[0]?.created_at || null;
  } catch (error) {
    console.error('Error in getLastRecordDate:', error);
    return null;
  }
}

export async function onRequest(context: any) {
  // Updated CORS headers
  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, HEAD, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400',
  };

  // Handle CORS preflight
  if (context.request.method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    // Initialize Supabase client
    const supabase = createClient(
      context.env.SUPABASE_URL!,
      context.env.SUPABASE_ANON_KEY!
    )

    // Get the last record date
    const lastRecordDate = await getLastRecordDate(supabase, context.env.SUPABASE_TABLE_STORIES!);
    console.log('Last record date:', lastRecordDate);

    // Get query parameters
    const url = new URL(context.request.url);
    const source = url.searchParams.get('source');
    const limit = url.searchParams.get('limit');
    const dateParam = url.searchParams.get('date');
    const id = url.searchParams.get('id');

    // Use the last record date if no date parameter is provided
    let date: Date;
    if (dateParam) {
      if (dateParam.includes('-') && !dateParam.includes('T')) {
        console.log("dateParam.includes('-') && !dateParam.includes('T') date: ", dateParam)
        date = new Date(dateParam + 'T00:00:00');
      } else {
        date = new Date(dateParam);
        console.log("new Date(dateParam) date: ", dateParam)
      }
    } else if (lastRecordDate) {
      // Use last record date (with) or current date as fallback
      const dateString = lastRecordDate.split('T')[0]
      console.log("lastRecordDate.split('T')[0] dateString: ", dateString)
      date = new Date(`${dateString}T00:00:00`)
      console.log("new Date(`${dateString}T00:00:00`) date: ", date)
    } else {
      date = new Date();
      console.log("new Date() date: ", date)
    }

    console.log('date', date);
    const startOfDay = new Date(date.getFullYear(), date.getMonth(), date.getDate()).toISOString()
    const endOfDay = new Date(date.getFullYear(), date.getMonth(), date.getDate() + 1).toISOString()
    console.log('startOfDay', startOfDay);
    console.log('endOfDay', endOfDay);

    // Prepare query
    let query = supabase
      .from(context.env.SUPABASE_TABLE_STORIES!)
      .select('*')
      .not('deleted', 'is', true) // filter out deleted is not true

    // If ID is provided, only search by ID
    if (id) {
      query = query.eq('id', id);
    } else {
      // Apply date and source filters only when not searching by ID
      query = query
        .gte('created_at', startOfDay)
        .lt('created_at', endOfDay)
        .not('source', 'is', null)
        .order('source', { ascending: true })
        .order('score', { ascending: false })

      // Add source filter if provided
      if (source) {
        query = query.eq('source', source)
      }

      // Apply limit only when not searching by ID
      query = query.limit(limit ? parseInt(limit) : 30)
    }
    // Execute query
    const { data, error } = await query;

    if (error) {
      return new Response(JSON.stringify({ error: error.message }), {
        status: 500,
        headers: {
          ...corsHeaders,
          'Content-Type': 'application/json',
        }
      })
    }

    // Count by source - only count if source exists and is not empty
    const countBySource = data?.reduce((acc: any, story: any) => {
      if (story?.source) {
        const sourceKey = story.source.toLowerCase();
        acc[sourceKey] = (acc[sourceKey] || 0) + 1;
      }
      return acc;
    }, {});

    // add cover to each story
    const stories = data?.map((story: any) => {
      if (story?.source) {
        story.cover = getTrackCover(story.source);
      } else {
        story.cover = ''; // or provide a default cover
      }
      return story;
    });

    // Initialize empty tracks array
    const tracks: Track[] = [];
    
    // Only process audio tracks if there are stories with audio URLs
    if (data && data.length > 0) {
      data.forEach((story: any) => {
        const cover = story?.source ? getTrackCover(story.source) : ''; // default empty string if no source
        // Push speech URL track
        if (story?.speech_url) {
          tracks.push({
            id: story.story_id?.toString() + "_audio",
            cover: cover,
            title: story.title || '',
            type: "Article audio",
            audioUrl: story.speech_url,
            createdAt: story.created_at
          });
        }
        
        // Push notebook URL track
        if (story?.notebooklm_url) {
          tracks.push({
            id: story.story_id?.toString() + "_podcast",
            cover: cover,
            title: story.title || '',
            type: "AI-generated podcast",
            audioUrl: story.notebooklm_url,
            createdAt: story.created_at,
          });
        }
      });
    }

    const result = {stories: stories || [], audioTracks: tracks || [], countBySource: countBySource}
    return new Response(JSON.stringify(result), {
      status: 200,
      headers: {
        ...corsHeaders,
        'Content-Type': 'application/json',
      }
    })

  } catch (err) {
    return new Response(JSON.stringify({ error: `Internal Server Error ${err}` }), {
      status: 500,
      headers: {
        ...corsHeaders,
        'Content-Type': 'application/json',
      }
    })
  }
}