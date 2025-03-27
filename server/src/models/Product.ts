import mongoose, { Schema, Document } from 'mongoose';

export interface IProduct extends Document {
  name: string;
  description: string;
  basePrice: number;
  currentPrice: number;
  category: string;
  brand: string;
  url: string;
  lastUpdated: Date;
  priceHistory: {
    price: number;
    date: Date;
  }[];
  competitorPrices: {
    source: string;
    price: number;
    lastChecked: Date;
  }[];
  pricingRules: {
    minPrice: number;
    maxPrice: number;
    targetMargin: number;
  };
}

const ProductSchema: Schema = new Schema({
  name: { type: String, required: true },
  description: { type: String, required: true },
  basePrice: { type: Number, required: true },
  currentPrice: { type: Number, required: true },
  category: { type: String, required: true },
  brand: { type: String, required: true },
  url: { type: String, required: true },
  lastUpdated: { type: Date, default: Date.now },
  priceHistory: [{
    price: { type: Number, required: true },
    date: { type: Date, default: Date.now }
  }],
  competitorPrices: [{
    source: { type: String, required: true },
    price: { type: Number, required: true },
    lastChecked: { type: Date, default: Date.now }
  }],
  pricingRules: {
    minPrice: { type: Number, required: true },
    maxPrice: { type: Number, required: true },
    targetMargin: { type: Number, required: true }
  }
});

export default mongoose.model<IProduct>('Product', ProductSchema); 