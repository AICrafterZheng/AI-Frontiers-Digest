import { createClient } from '@supabase/supabase-js'
import { constructResult } from '../../src/lib/utils';

export async function onRequest(context: any) {
  // CORS headers
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

    // Get query parameters
    const url = new URL(context.request.url);
    const query = url.searchParams.get('q');
    const limit = parseInt(url.searchParams.get('limit') || '10');

    if (!query) {
      return new Response(
        JSON.stringify({ error: 'Search query is required' }),
        { 
          status: 400,
          headers: {
            'Content-Type': 'application/json',
            ...corsHeaders
          }
        }
      );
    }

    // Split query into words for better matching
    const searchTerms = query.toLowerCase().split(/\s+/);
    
    // Prepare the search query using ilike for case-insensitive partial matches
    let dbQuery = supabase
      .from(context.env.SUPABASE_TABLE_STORIES!)
      .select('*')
      .not('deleted', 'is', true);

    // Add search conditions for each term
    searchTerms.forEach((term) => {
      dbQuery = dbQuery.ilike('title', `%${term}%`);
    });

    // Add limit and order by creation date
    const { data, error } = await dbQuery
      .order('created_at', { ascending: false })
      .limit(limit);

    if (error) {
      console.error('Error searching stories:', error);
      return new Response(
        JSON.stringify({ error: 'Failed to search stories' }),
        { 
          status: 500,
          headers: {
            'Content-Type': 'application/json',
            ...corsHeaders
          }
        }
      );
    }
    const results = constructResult(data);
    // Return the search results
    return new Response(
      JSON.stringify(results),
      { 
        headers: {
          'Content-Type': 'application/json',
          ...corsHeaders
        }
      }
    );

  } catch (error) {
    console.error('Error in search API:', error);
    return new Response(
      JSON.stringify({ error: 'Internal server error' }),
      { 
        status: 500,
        headers: {
          'Content-Type': 'application/json',
          ...corsHeaders
        }
      }
    );
  }
}
