
import React from 'react';
import { ArrowUpRight, ArrowDownRight, ArrowRight } from 'lucide-react';
import { Product } from '../data/mockData';

interface ProductCardProps {
  product: Product;
  onClick: (product: Product) => void;
}

const ProductCard: React.FC<ProductCardProps> = ({ product, onClick }) => {
  const priceChange = product.currentPrice - product.previousPrice;
  const priceChangePercent = (priceChange / product.previousPrice) * 100;
  
  const getPriceIndicator = () => {
    if (priceChange > 0) {
      return <ArrowUpRight className="h-4 w-4 text-green-500" />;
    } else if (priceChange < 0) {
      return <ArrowDownRight className="h-4 w-4 text-red-500" />;
    } else {
      return <ArrowRight className="h-4 w-4 text-gray-400" />;
    }
  };

  const getPriceChangeClass = () => {
    if (priceChange > 0) return 'text-green-600';
    if (priceChange < 0) return 'text-red-600';
    return 'text-gray-600';
  };

  return (
    <div 
      className="group bg-white rounded-xl overflow-hidden border border-gray-100 shadow-sm hover:shadow-md transition-all duration-300 hover:translate-y-[-2px] cursor-pointer animate-scale-in"
      onClick={() => onClick(product)}
    >
      <div className="relative">
        <img 
          src={product.image} 
          alt={product.name} 
          className="w-full h-48 object-cover transition-transform duration-500 group-hover:scale-105"
        />
        <div className="absolute top-2 right-2 bg-black/60 text-white text-xs px-2 py-1 rounded-full backdrop-blur-sm">
          Stock: {product.inStock}
        </div>
      </div>
      <div className="p-4">
        <div className="flex justify-between items-start mb-2">
          <h3 className="font-medium text-gray-900 group-hover:text-gray-700 transition-colors">
            {product.name}
          </h3>
          <span className="text-xs font-medium px-2 py-1 bg-gray-100 rounded-full">
            {product.category}
          </span>
        </div>
        
        <div className="flex justify-between items-center mb-3">
          <div className="text-xl font-semibold">${product.currentPrice.toFixed(2)}</div>
          <div className="flex items-center space-x-1">
            {getPriceIndicator()}
            <span className={`text-xs font-medium ${getPriceChangeClass()}`}>
              {Math.abs(priceChangePercent).toFixed(1)}%
            </span>
          </div>
        </div>
        
        <div className="text-sm text-gray-600 flex justify-between items-center">
          <div>
            <span className="mr-1">AI Suggests:</span>
            <span className="font-medium">${product.suggestedPrice.toFixed(2)}</span>
          </div>
          <span className="text-xs px-2 py-1 rounded-full bg-blue-50 text-blue-700">
            {product.competitors.length} competitors
          </span>
        </div>
      </div>
    </div>
  );
};

export default ProductCard;
