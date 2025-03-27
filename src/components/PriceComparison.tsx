
import React from 'react';
import { ArrowUpRight, ArrowDownRight, Minus, Check, X } from 'lucide-react';
import { Product, CompetitorPrice } from '../data/mockData';

interface PriceComparisonProps {
  product: Product;
}

const PriceComparison: React.FC<PriceComparisonProps> = ({ product }) => {
  const getSuggestedAction = () => {
    if (product.suggestedPrice < product.currentPrice) {
      return {
        text: 'Decrease Price',
        indicator: <ArrowDownRight className="h-4 w-4 text-red-500" />,
        class: 'text-red-700 bg-red-50'
      };
    } else if (product.suggestedPrice > product.currentPrice) {
      return {
        text: 'Increase Price',
        indicator: <ArrowUpRight className="h-4 w-4 text-green-500" />,
        class: 'text-green-700 bg-green-50'
      };
    } else {
      return {
        text: 'Maintain Price',
        indicator: <Minus className="h-4 w-4 text-gray-500" />,
        class: 'text-gray-700 bg-gray-50'
      };
    }
  };

  const getCompetitorPriceComparison = (competitor: CompetitorPrice) => {
    const priceDiff = product.currentPrice - competitor.price;
    if (priceDiff > 0) {
      return { text: 'Higher than competitor', class: 'text-red-600' };
    } else if (priceDiff < 0) {
      return { text: 'Lower than competitor', class: 'text-green-600' };
    } else {
      return { text: 'Same as competitor', class: 'text-gray-600' };
    }
  };

  const action = getSuggestedAction();

  return (
    <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5 animate-fade-in">
      <h3 className="text-lg font-medium text-gray-900 mb-4">Price Comparison</h3>
      
      <div className="mb-6">
        <div className="flex justify-between items-center mb-2">
          <span className="text-gray-600">Current Price</span>
          <span className="font-semibold">${product.currentPrice.toFixed(2)}</span>
        </div>
        <div className="flex justify-between items-center mb-2">
          <span className="text-gray-600">Previous Price</span>
          <span>${product.previousPrice.toFixed(2)}</span>
        </div>
        <div className="flex justify-between items-center mb-2">
          <span className="text-gray-600">AI Suggested Price</span>
          <span className="font-medium">${product.suggestedPrice.toFixed(2)}</span>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-gray-600">Recommended Action</span>
          <div className={`flex items-center space-x-1 px-2 py-1 rounded-full text-xs font-medium ${action.class}`}>
            {action.indicator}
            <span>{action.text}</span>
          </div>
        </div>
      </div>

      <h4 className="text-sm font-medium text-gray-900 mb-3">Competitor Prices</h4>
      {product.competitors.map((competitor, index) => (
        <div key={index} className="py-3 border-t border-gray-100">
          <div className="flex justify-between items-center mb-1">
            <span className="font-medium">{competitor.name}</span>
            <span className="font-medium">${competitor.price.toFixed(2)}</span>
          </div>
          <div className="flex justify-between items-center text-xs">
            <div className="flex items-center">
              {competitor.inStock ? 
                <Check className="h-3 w-3 text-green-500 mr-1" /> : 
                <X className="h-3 w-3 text-red-500 mr-1" />
              }
              <span className="text-gray-600">{competitor.inStock ? 'In stock' : 'Out of stock'}</span>
            </div>
            <span className={getCompetitorPriceComparison(competitor).class}>
              {getCompetitorPriceComparison(competitor).text}
            </span>
          </div>
        </div>
      ))}
    </div>
  );
};

export default PriceComparison;
