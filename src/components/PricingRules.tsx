
import React, { useState } from 'react';
import { Product, PricingRule } from '@/types/supabase';
import { priceAdjustmentReasons } from '../data/mockData';
import { Check } from 'lucide-react';
import { applyPricingRule } from '@/services/productService';
import { toast } from 'sonner';

interface PricingRulesProps {
  product: Product;
  onApplyRules: (productId: string, rules: string[], newPrice: number) => void;
}

const PricingRules: React.FC<PricingRulesProps> = ({ product, onApplyRules }) => {
  const [selectedRules, setSelectedRules] = useState<string[]>([]);
  const [customPrice, setCustomPrice] = useState<string>(
    product?.current_price ? product.current_price.toString() : '0'
  );
  const [isApplying, setIsApplying] = useState(false);
  
  const handleRuleToggle = (ruleId: string) => {
    setSelectedRules(prev => 
      prev.includes(ruleId) 
        ? prev.filter(id => id !== ruleId) 
        : [...prev, ruleId]
    );
  };
  
  const handleApplyRules = async () => {
    if (!product) return;
    
    setIsApplying(true);
    
    try {
      const success = await applyPricingRule(
        product.id,
        selectedRules.length > 0 ? selectedRules.join(',') : 'manual_price_change',
        parseFloat(customPrice)
      );
      
      if (success) {
        onApplyRules(product.id, selectedRules, parseFloat(customPrice));
      }
    } catch (error) {
      console.error('Error applying pricing rules:', error);
      toast.error('Failed to apply pricing rules');
    } finally {
      setIsApplying(false);
    }
  };

  if (!product) {
    return <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
      No product selected
    </div>;
  }

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
          disabled={
            (selectedRules.length === 0 && 
             parseFloat(customPrice) === product.current_price) || 
            isApplying
          }
          className={`w-full px-4 py-2 rounded-md text-white font-medium transition-colors ${
            (selectedRules.length > 0 || parseFloat(customPrice) !== product.current_price) && !isApplying
              ? 'bg-blue-600 hover:bg-blue-700' 
              : 'bg-gray-300 cursor-not-allowed'
          }`}
        >
          {isApplying ? 'Applying...' : 'Apply Pricing Rules'}
        </button>
      </div>
    </div>
  );
};

export default PricingRules;
