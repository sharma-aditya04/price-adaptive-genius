
// Custom types for our database tables
// We define these separately from the generated Supabase types

export interface Product {
  id: string;
  name: string;
  current_price: number;
  previous_price?: number;
  suggested_price?: number;
  category?: string;
  image_url?: string;
  in_stock?: number;
  created_at?: string;
  updated_at?: string;
}

export interface CompetitorPrice {
  id: string;
  product_id: string;
  competitor_name: string;
  price: number;
  in_stock?: boolean;
  created_at?: string;
}

export interface PriceHistory {
  id: string;
  product_id: string;
  price: number;
  date?: string;
}

export interface PricingRule {
  id: string;
  product_id: string;
  rule_id: string;
  applied_at?: string;
}
