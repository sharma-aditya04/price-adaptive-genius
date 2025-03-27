
import React, { useState } from 'react';
import { Product, priceAdjustmentReasons } from '../data/mockData';
import { Check } from 'lucide-react';

interface PricingRulesProps {
  product: Product;
  onApplyRules: (productId: number, rules: string[], newPrice: number) => void;
}

const PricingRules: React.FC<PricingRulesProps> = ({ product, onApplyRules }) => {
  const [selectedRules, setSelectedRules] = useState<string[]>([]);
  const [customPrice, setCustomPrice] = useState<string>(product.currentPrice.toFixed(2));
  
  const handleRuleToggle = (ruleId: string) => {
    setSelectedRules(prev => 
      prev.includes(ruleId) 
        ? prev.filter(id => id !== ruleId) 
        : [...prev, ruleId]
    );
  };
  
  const handleApplyRules = () => {
    onApplyRules(product.id, selectedRules, parseFloat(customPrice));
  };

  return (
    <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5 animate-fade-in">
      <h3 className="text-lg font-medium text-gray-900 mb-4">Custom Pricing Rules</h3>
      
      <div className="space-y-3 mb-6">
        {priceAdjustmentReasons.map((rule) => (
          <div 
            key={rule.id}
            className="flex items-center"
          >
            <button
              onClick={() => handleRuleToggle(rule.id)}
              className={`w-5 h-5 rounded border mr-3 flex items-center justify-center transition-colors ${
                selectedRules.includes(rule.id) 
                  ? 'bg-blue-600 border-blue-600 text-white' 
                  : 'border-gray-300 text-transparent'
              }`}
            >
              <Check className="h-3 w-3" />
            </button>
            <span className="text-gray-700">{rule.label}</span>
          </div>
        ))}
      </div>
      
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Custom Price
        </label>
        <div className="flex">
          <span className="inline-flex items-center px-3 rounded-l-md border border-r-0 border-gray-300 bg-gray-50 text-gray-500">
            $
          </span>
          <input
            type="number"
            step="0.01"
            value={customPrice}
            onChange={(e) => setCustomPrice(e.target.value)}
            className="flex-1 min-w-0 block w-full px-3 py-2 rounded-none rounded-r-md border border-gray-300 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            placeholder="0.00"
          />
        </div>
      </div>
      
      <div>
        <button
          onClick={handleApplyRules}
          className={`w-full px-4 py-2 rounded-md text-white font-medium transition-colors ${
            selectedRules.length > 0 || parseFloat(customPrice) !== product.currentPrice
              ? 'bg-blue-600 hover:bg-blue-700' 
              : 'bg-gray-300 cursor-not-allowed'
          }`}
          disabled={selectedRules.length === 0 && parseFloat(customPrice) === product.currentPrice}
        >
          Apply Pricing Rules
        </button>
      </div>
    </div>
  );
};

export default PricingRules;
