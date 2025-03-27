
import { supabase } from "@/integrations/supabase/client";
import { Product, CompetitorPrice, PriceHistory, PricingRule } from "@/types/supabase";
import { toast } from "sonner";

// Product CRUD operations
export const fetchProducts = async (): Promise<Product[]> => {
  try {
    const { data, error } = await supabase
      .from('products')
      .select('*');
    
    if (error) throw error;
    return data || [];
  } catch (error) {
    console.error('Error fetching products:', error);
    toast.error('Failed to fetch products');
    return [];
  }
};

export const fetchProductById = async (id: string): Promise<Product | null> => {
  try {
    const { data, error } = await supabase
      .from('products')
      .select('*')
      .eq('id', id)
      .single();
    
    if (error) throw error;
    return data;
  } catch (error) {
    console.error(`Error fetching product ${id}:`, error);
    toast.error('Failed to fetch product details');
    return null;
  }
};

export const createProduct = async (product: Omit<Product, 'id' | 'created_at' | 'updated_at'>): Promise<Product | null> => {
  try {
    const { data, error } = await supabase
      .from('products')
      .insert([product])
      .select()
      .single();
    
    if (error) throw error;
    
    // Also add to price history
    if (data) {
      await supabase.from('price_history').insert([{
        product_id: data.id,
        price: data.current_price
      }]);
    }
    
    toast.success('Product created successfully');
    return data;
  } catch (error) {
    console.error('Error creating product:', error);
    toast.error('Failed to create product');
    return null;
  }
};

export const updateProduct = async (id: string, updates: Partial<Product>): Promise<Product | null> => {
  try {
    // First get the current product to check if price changed
    const { data: currentProduct } = await supabase
      .from('products')
      .select('current_price')
      .eq('id', id)
      .single();
    
    // Add updated_at timestamp
    const updatedData = { ...updates, updated_at: new Date().toISOString() };
    
    const { data, error } = await supabase
      .from('products')
      .update(updatedData)
      .eq('id', id)
      .select()
      .single();
    
    if (error) throw error;
    
    // If price was updated, add to price history
    if (data && updates.current_price && currentProduct && updates.current_price !== currentProduct.current_price) {
      await supabase.from('price_history').insert([{
        product_id: id,
        price: updates.current_price
      }]);
    }
    
    toast.success('Product updated successfully');
    return data;
  } catch (error) {
    console.error(`Error updating product ${id}:`, error);
    toast.error('Failed to update product');
    return null;
  }
};

export const deleteProduct = async (id: string): Promise<boolean> => {
  try {
    const { error } = await supabase
      .from('products')
      .delete()
      .eq('id', id);
    
    if (error) throw error;
    toast.success('Product deleted successfully');
    return true;
  } catch (error) {
    console.error(`Error deleting product ${id}:`, error);
    toast.error('Failed to delete product');
    return false;
  }
};

// Competitor prices operations
export const fetchCompetitorPrices = async (productId: string): Promise<CompetitorPrice[]> => {
  try {
    const { data, error } = await supabase
      .from('competitor_prices')
      .select('*')
      .eq('product_id', productId);
    
    if (error) throw error;
    return data || [];
  } catch (error) {
    console.error(`Error fetching competitor prices for product ${productId}:`, error);
    toast.error('Failed to fetch competitor data');
    return [];
  }
};

// Price history operations
export const fetchPriceHistory = async (productId: string): Promise<PriceHistory[]> => {
  try {
    const { data, error } = await supabase
      .from('price_history')
      .select('*')
      .eq('product_id', productId)
      .order('date', { ascending: false });
    
    if (error) throw error;
    return data || [];
  } catch (error) {
    console.error(`Error fetching price history for product ${productId}:`, error);
    toast.error('Failed to fetch price history');
    return [];
  }
};

// Pricing rules operations
export const applyPricingRule = async (productId: string, ruleId: string, newPrice: number): Promise<boolean> => {
  try {
    // Begin transaction
    const { data: product, error: productError } = await supabase
      .from('products')
      .select('current_price')
      .eq('id', productId)
      .single();
    
    if (productError) throw productError;
    
    // Update product price
    const { error: updateError } = await supabase
      .from('products')
      .update({ 
        previous_price: product.current_price,
        current_price: newPrice,
        updated_at: new Date().toISOString()
      })
      .eq('id', productId);
      
    if (updateError) throw updateError;
    
    // Record the rule application
    const { error: ruleError } = await supabase
      .from('pricing_rules')
      .insert([{ product_id: productId, rule_id: ruleId }]);
      
    if (ruleError) throw ruleError;
    
    // Add to price history
    const { error: historyError } = await supabase
      .from('price_history')
      .insert([{ product_id: productId, price: newPrice }]);
      
    if (historyError) throw historyError;
    
    toast.success('Pricing rule applied successfully');
    return true;
  } catch (error) {
    console.error(`Error applying pricing rule to product ${productId}:`, error);
    toast.error('Failed to apply pricing rule');
    return false;
  }
};
