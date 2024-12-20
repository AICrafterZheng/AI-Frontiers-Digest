import { createClient } from '@supabase/supabase-js'
import { ARCHIVE_LIST_DAYS } from '../../src/lib/constants';

interface SourceStats {
  [source: string]: number;
}

// Add this date handling logic to match news.ts
const getDateRange = (endDate: Date) => {
  const startDate = new Date(endDate);
  startDate.setDate(startDate.getDate() - ARCHIVE_LIST_DAYS);
  
  const startOfDay = new Date(startDate.getFullYear(), startDate.getMonth(), startDate.getDate()).toISOString();
  const endOfDay = new Date(endDate.getFullYear(), endDate.getMonth(), endDate.getDate() + 1).toISOString();
  
  return { startOfDay, endOfDay };
};

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

    // Calculate date range using the same logic as news.ts
    const endDate = new Date();
    const { startOfDay, endOfDay } = getDateRange(endDate);
    console.log('startOfDay', startOfDay);
    console.log('endOfDay', endOfDay);

    // Update the query to use the same date format
    const { data, error } = await supabase
      .from(context.env.SUPABASE_TABLE_STORIES!)
      .select('created_at, source')
      .gte('created_at', startOfDay)
      .lt('created_at', endOfDay);

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

    // Sort by date in descending order using Date objects
    const sortedStats = Object.fromEntries(
      Object.entries(stats).sort(([a], [b]) => {
        const dateA = new Date(a);
        const dateB = new Date(b);
        return dateB.getTime() - dateA.getTime();
      })
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