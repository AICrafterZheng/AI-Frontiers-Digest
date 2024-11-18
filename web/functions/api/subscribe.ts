import { createClient } from '@supabase/supabase-js';

export const onRequest = async (context: any) => {
  // CORS headers for local development and production
  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  };

  // Handle CORS preflight
  if (context.request.method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    const { email } = await context.request.json();
    // Initialize Supabase
    const supabase = createClient(
      context.env.SUPABASE_URL,
      context.env.SUPABASE_ANON_KEY
    );
    // Check for existing subscriber and unsubscribed field is false
    const { data: existingSubscriber } = await supabase
      .from(context.env.SUPABASE_TABLE_SUBSCRIBERS)
      .select()
      .eq('email', email)
      .eq('unsubscribed', false)
      .single();

    if (existingSubscriber) {
      return new Response(
        JSON.stringify({ error: 'Email already subscribed' }),
        { 
          status: 409, 
          headers: { ...corsHeaders, 'Content-Type': 'application/json' } 
        }
      );
    }

    // Add new subscriber or update unsubscribed field to false
    const { data: subscriber, error } = await supabase
      .from(context.env.SUPABASE_TABLE_SUBSCRIBERS)
      .upsert([{ email, unsubscribed: false }], { onConflict: 'email' })
      .select()
      .single();

    if (error) throw error;

    return new Response(
      JSON.stringify({ message: 'Successfully subscribed', subscriber }), 
      { 
        status: 201, 
        headers: { ...corsHeaders, 'Content-Type': 'application/json' } 
      }
    );

  } catch (error) {
    console.error('Subscription error:', error);
    return new Response(
      JSON.stringify({ error: `Internal server error` }), 
      { 
        status: 500, 
        headers: { ...corsHeaders, 'Content-Type': 'application/json' } 
      }
    );
  }
};