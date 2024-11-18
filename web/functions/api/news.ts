import { createClient } from '@supabase/supabase-js'

async function getHNScore(id: string): Promise<number> {
  try {
    const response = await fetch(`https://hacker-news.firebaseio.com/v0/item/${id}.json`);
    const data = await response.json();
    return data.score || 0;
  } catch (error) {
    console.error('Error fetching HN score:', error);
    return 0;
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
    // Get the source from query parameters
    const url = new URL(context.request.url)
    const source = url.searchParams.get('source')
    const limit = url.searchParams.get('limit')
    
    // Get the date from query parameters
    const dateParam = url.searchParams.get('date') // format: 2024-11-01
    // Parse the date and create UTC boundaries
    const date = dateParam ? new Date(dateParam) : new Date()
    const startOfDay = new Date(Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate())).toISOString()
    const endOfDay = new Date(Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate() + 1)).toISOString()

    // Start building the query
    let query = supabase
      .from(context.env.SUPABASE_TABLE_STORIES!)
      .select('*')
      .gte('created_at', startOfDay)
      .lt('created_at', endOfDay)

    // Add source filter if provided
    if (source) {
      query = query.eq('source', source)
    }

    // Execute the query with ordering and limit
    let { data, error } = await query
      .not('source', 'is', null)
      .order('source', { ascending: true })
      .order('score', { ascending: false })
      .limit(limit ? parseInt(limit) : 30)

    if (error) {
      return new Response(JSON.stringify({ error: error.message }), {
        status: 500,
        headers: {
          ...corsHeaders,
          'Content-Type': 'application/json',
        }
      })
    }

    // If source is HN, update scores before returning
    if (data && data.length > 0) {
      const updatedData = await Promise.all(
        data.map(async (story: any) => {
          if (story.source.toLowerCase() === 'hackernews') {
            const score = await getHNScore(story.story_id);
            // Update the score in database if it changed
            if (score !== story.score) {
              await supabase
                .from(context.env.SUPABASE_TABLE_STORIES!)
                .update({ score })
                .eq('id', story.id);
            }
            return { ...story, score };
          }
          return story;
        })
      );
      data = updatedData;
    }
    return new Response(JSON.stringify(data || []), {
      status: 200,
      headers: {
        ...corsHeaders,
        'Content-Type': 'application/json',
      }
    })

  } catch (err) {
    return new Response(JSON.stringify({ error: 'Internal Server Error' }), {
      status: 500,
      headers: {
        ...corsHeaders,
        'Content-Type': 'application/json',
      }
    })
  }
}