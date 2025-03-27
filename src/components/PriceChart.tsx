
import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Product } from '@/types/supabase';
import { fetchPriceHistory } from '@/services/productService';
import { format } from 'date-fns';

interface PriceChartProps {
  product: Product;
}

const PriceChart: React.FC<PriceChartProps> = ({ product }) => {
  const [priceHistory, setPriceHistory] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const loadPriceHistory = async () => {
      setIsLoading(true);
      try {
        const data = await fetchPriceHistory(product.id);
        
        // Convert date strings to formatted dates for display
        const formattedData = data.map(item => ({
          ...item,
          displayDate: format(new Date(item.date || ''), 'MMM d')
        }));
        
        setPriceHistory(formattedData);
      } catch (error) {
        console.error('Error loading price history:', error);
      } finally {
        setIsLoading(false);
      }
    };
    
    loadPriceHistory();
  }, [product.id]);

  // Add current price and AI suggested price to historical data for visualization
  const getChartData = () => {
    const historyData = priceHistory.map(item => ({
      date: item.displayDate,
      price: item.price
    }));
    
    return [
      ...historyData,
      { date: 'Current', price: product.current_price },
      ...(product.suggested_price ? [{ date: 'AI Suggested', price: product.suggested_price }] : [])
    ];
  };

  const chartData = getChartData();

  // Get min and max for the domain
  const prices = chartData.map(item => item.price);
  const minPrice = Math.min(...prices) * 0.95; // 5% buffer below min
  const maxPrice = Math.max(...prices) * 1.05; // 5% buffer above max

  return (
    <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5 animate-fade-in">
      <h3 className="text-lg font-medium text-gray-900 mb-4">Price History</h3>
      
      {isLoading ? (
        <div className="h-[200px] flex items-center justify-center">
          <p className="text-gray-500">Loading price history...</p>
        </div>
      ) : chartData.length > 1 ? (
        <div className="h-[200px]">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={chartData}
              margin={{
                top: 5,
                right: 5,
                left: 5,
                bottom: 5,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#f5f5f5" />
              <XAxis 
                dataKey="date" 
                tick={{ fontSize: 12 }}
                tickLine={false}
              />
              <YAxis 
                domain={[minPrice, maxPrice]}
                tick={{ fontSize: 12 }}
                tickLine={false}
                tickFormatter={(value) => `$${value.toFixed(0)}`}
              />
              <Tooltip 
                formatter={(value) => [`$${Number(value).toFixed(2)}`, 'Price']}
                contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 2px 8px rgba(0, 0, 0, 0.15)' }}
              />
              <Line 
                type="monotone" 
                dataKey="price" 
                stroke="#4f46e5" 
                strokeWidth={2}
                dot={{ stroke: '#4f46e5', strokeWidth: 2, r: 4, fill: 'white' }}
                activeDot={{ r: 6, stroke: '#4f46e5', strokeWidth: 2, fill: '#4f46e5' }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      ) : (
        <div className="h-[200px] flex items-center justify-center">
          <p className="text-gray-500">Not enough price history data available</p>
        </div>
      )}
      
      <div className="mt-4 grid grid-cols-2 gap-2 text-xs text-gray-600">
        <div className="flex flex-col">
          <span>Average Price</span>
          <span className="font-medium text-gray-900">
            ${prices.length > 0 ? (prices.reduce((a, b) => a + b, 0) / prices.length).toFixed(2) : '-'}
          </span>
        </div>
        <div className="flex flex-col">
          <span>Price Volatility</span>
          <span className="font-medium text-gray-900">
            {priceHistory.length > 1 ? 
              Math.abs((product.current_price - priceHistory[priceHistory.length - 1].price) / priceHistory[priceHistory.length - 1].price * 100).toFixed(1) + '%' : 
              'N/A'}
          </span>
        </div>
      </div>
    </div>
  );
};

export default PriceChart;
