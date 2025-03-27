
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2.21.0'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

serve(async (req) => {
  // Handle CORS preflight requests
  if (req.method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders })
  }
  
  try {
    const url = Deno.env.get('SUPABASE_URL') || '';
    const key = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') || '';
    const supabase = createClient(url, key);
    
    const { id, competitorPrices } = await req.json();
    
    if (!id) {
      return new Response(
        JSON.stringify({ error: 'Product ID is required' }),
        { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 400 }
      )
    }
    
    // Fetch product data
    const { data: product, error: productError } = await supabase
      .from('products')
      .select('*')
      .eq('id', id)
      .single();
      
    if (productError) {
      return new Response(
        JSON.stringify({ error: 'Product not found' }),
        { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 404 }
      )
    }
    
    // Fetch competitor prices if not provided
    let competitors = competitorPrices;
    if (!competitors) {
      const { data: fetchedCompetitors, error: competitorsError } = await supabase
        .from('competitor_prices')
        .select('*')
        .eq('product_id', id);
        
      if (!competitorsError) {
        competitors = fetchedCompetitors;
      }
    }
    
    // Fetch price history
    const { data: priceHistory, error: historyError } = await supabase
      .from('price_history')
      .select('*')
      .eq('product_id', id)
      .order('date', { ascending: false })
      .limit(10);
    
    // Simplistic AI price prediction model
    // In a real scenario, this would use a more sophisticated ML model
    const calculateSuggestedPrice = () => {
      // Start with current price
      let basePrice = product.current_price;
      
      // Factor 1: Competitor pricing (weighted average)
      if (competitors && competitors.length > 0) {
        const avgCompetitorPrice = competitors.reduce((sum, comp) => sum + comp.price, 0) / competitors.length;
        // Weight: 40% competitor influence
        basePrice = basePrice * 0.6 + avgCompetitorPrice * 0.4;
      }
      
      // Factor 2: Price trend from history
      if (priceHistory && priceHistory.length > 1) {
        const recentTrend = priceHistory[0].price - priceHistory[priceHistory.length - 1].price;
        // Slight influence from trend (5%)
        basePrice += recentTrend * 0.05;
      }
      
      // Factor 3: Stock availability
      if (product.in_stock !== undefined && product.in_stock < 10) {
        // Low stock might justify slightly higher price (up to 5%)
        basePrice *= (1 + (0.05 * (1 - product.in_stock / 10)));
      }
      
      // Round to 2 decimal places for currency
      return Math.round(basePrice * 100) / 100;
    };
    
    const suggestedPrice = calculateSuggestedPrice();
    
    // Update the product with the suggested price
    await supabase
      .from('products')
      .update({ suggested_price: suggestedPrice })
      .eq('id', id);
    
    return new Response(
      JSON.stringify({ 
        suggestedPrice, 
        currentPrice: product.current_price,
        factors: {
          competitorCount: competitors?.length || 0,
          priceHistoryCount: priceHistory?.length || 0,
          inStock: product.in_stock
        }
      }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )
  } catch (error) {
    console.error('Error in price prediction:', error);
    return new Response(
      JSON.stringify({ error: error.message }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 500 }
    )
  }
})
