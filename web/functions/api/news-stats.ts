import { createClient } from '@supabase/supabase-js'

interface SourceStats {
  [source: string]: number;
}

export async function onRequest(context: any) {
  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, HEAD, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400',
  };

  if (context.request.method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    const supabase = createClient(
      context.env.SUPABASE_URL!,
      context.env.SUPABASE_ANON_KEY!
    )

    // Calculate date range (10 days ago from now)
    const endDate = new Date();
    console.log('endDate', endDate);
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - 2);
    console.log('startDate', startDate);

    // Query to get all news within date range
    const { data, error } = await supabase
      .from(context.env.SUPABASE_TABLE_STORIES!)
      .select('created_at, source')
      .gte('created_at', startDate.toISOString())
      .lte('created_at', endDate.toISOString());

    if (error) {
      throw error;
    }

    // Get unique sources
    const sources = new Set<string>();
    data.forEach((item: any) => {
      if (item.source) {
        sources.add(item.source.toLowerCase());
      }
    });

    // Process the data to group by date and source
    const stats: Record<string, SourceStats> = {};

    data.forEach((item: any) => {
      if (!item.created_at || !item.source) return;
      
      // const date = new Date(item.created_at).toISOString().split('T')[0];
      const date = new Date(item.created_at).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
      const source = item.source.toLowerCase();
      // Initialize the date if it doesn't exist
      if (!stats[date]) {
        stats[date] = Array.from(sources).reduce((acc, src) => {
          acc[src] = 0;
          return acc;
        }, {} as SourceStats);
      }
      
      // Increment the counter
      stats[date][source] += 1;
    });

    // Sort by date in descending order
    const sortedStats = Object.fromEntries(
      Object.entries(stats).sort(([a], [b]) => b.localeCompare(a))
    );

    return new Response(JSON.stringify(sortedStats), {
      status: 200,
      headers: {
        ...corsHeaders,
        'Content-Type': 'application/json',
      }
    });

  } catch (err) {
    console.error('Error:', err);
    return new Response(JSON.stringify({ 
      error: 'Internal Server Error',
      details: err instanceof Error ? err.message : 'Unknown error'
    }), {
      status: 500,
      headers: {
        ...corsHeaders,
        'Content-Type': 'application/json',
      }
    });
  }
}