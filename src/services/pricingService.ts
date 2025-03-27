
import { supabase } from "@/integrations/supabase/client";
import { Product } from "@/types/supabase";
import { toast } from "sonner";

export const predictPrice = async (productId: string): Promise<number | null> => {
  try {
    const { data, error } = await supabase.functions.invoke('predict_price', {
      body: { id: productId },
    });
    
    if (error) throw error;
    
    if (data && data.suggestedPrice !== undefined) {
      toast.success('AI price suggestion generated');
      return data.suggestedPrice;
    }
    
    return null;
  } catch (error) {
    console.error('Error predicting price:', error);
    toast.error('Failed to generate price suggestion');
    return null;
  }
};

export const importCompetitorData = async (
  productId: string, 
  competitorData: Array<{ competitor_name: string; price: number; in_stock?: boolean }>
): Promise<boolean> => {
  try {
    // Delete existing competitor data for this product
    const { error: deleteError } = await supabase
      .from('competitor_prices')
      .delete()
      .eq('product_id', productId);
      
    if (deleteError) throw deleteError;
    
    // Insert new competitor data
    const { error: insertError } = await supabase
      .from('competitor_prices')
      .insert(competitorData.map(comp => ({
        product_id: productId,
        competitor_name: comp.competitor_name,
        price: comp.price,
        in_stock: comp.in_stock !== undefined ? comp.in_stock : true
      })));
      
    if (insertError) throw insertError;
    
    // Generate new price suggestion with the updated competitor data
    await predictPrice(productId);
    
    toast.success('Competitor data imported successfully');
    return true;
  } catch (error) {
    console.error('Error importing competitor data:', error);
    toast.error('Failed to import competitor data');
    return false;
  }
};
