import React, { useState } from 'react';
import { scrapeProduct } from '../services/scraperService';
import { toast } from 'sonner';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { ArrowRight } from 'lucide-react';
import { Product } from '../data/mockData';

const ProductScraper = () => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [productInfo, setProductInfo] = useState<any>(null);

  const handleScrape = async () => {
    if (!url) {
      toast.error('Please enter a product URL');
      return;
    }

    setLoading(true);
    try {
      const response = await scrapeProduct(url);
      if (response.error) {
        toast.error(response.error);
        return;
      }
      setProductInfo(response.data);
      toast.success('Product information scraped successfully');
    } catch (error) {
      toast.error('Failed to scrape product information');
    } finally {
      setLoading(false);
    }
  };

  // Convert scraped data to match Product type
  const convertToProduct = (data: any): Product => {
    const currentPrice = parseFloat(data.Price) || 0;
    return {
      id: Math.floor(Math.random() * 1000), // Generate a random ID
      name: data["Product Name"],
      currentPrice: currentPrice,
      previousPrice: currentPrice, // Since we don't have historical data
      suggestedPrice: currentPrice, // Since we don't have AI suggestions
      category: "Scraped", // Default category
      image: data["Image URL"] || "https://via.placeholder.com/500",
      inStock: data.Stock === "In Stock" ? 1 : 0,
      competitors: [], // No competitor data available
      priceHistory: [] // No price history available
    };
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Product Scraper</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="flex gap-2">
            <Input
              type="text"
              placeholder="Enter product URL (Amazon, Flipkart, Myntra, or AJIO)"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              className="flex-1"
            />
            <Button onClick={handleScrape} disabled={loading}>
              {loading ? 'Scraping...' : 'Scrape'}
            </Button>
          </div>

          {productInfo && (
            <div className="group bg-white rounded-xl overflow-hidden border border-gray-100 shadow-sm hover:shadow-md transition-all duration-300 hover:translate-y-[-2px] animate-scale-in">
              <div className="relative">
                <img 
                  src={productInfo["Image URL"]} 
                  alt={productInfo["Product Name"]} 
                  className="w-full h-48 object-cover transition-transform duration-500 group-hover:scale-105"
                />
                <div className="absolute top-2 right-2 bg-black/60 text-white text-xs px-2 py-1 rounded-full backdrop-blur-sm">
                  Stock: {productInfo.Stock}
                </div>
              </div>
              <div className="p-4">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-medium text-gray-900 group-hover:text-gray-700 transition-colors">
                    {productInfo["Product Name"]}
                  </h3>
                  <span className="text-xs font-medium px-2 py-1 bg-gray-100 rounded-full">
                    Scraped
                  </span>
                </div>
                
                <div className="flex justify-between items-center mb-3">
                  <div className="text-xl font-semibold">₹{productInfo.Price}</div>
                  <div className="flex items-center space-x-1">
                    <ArrowRight className="h-4 w-4 text-gray-400" />
                    <span className="text-xs font-medium text-gray-600">
                      0%
                    </span>
                  </div>
                </div>
                
                <div className="text-sm text-gray-600 flex justify-between items-center">
                  <div>
                    <span className="mr-1">AI Suggests:</span>
                    <span className="font-medium">₹{productInfo.Price}</span>
                  </div>
                  <span className="text-xs px-2 py-1 rounded-full bg-blue-50 text-blue-700">
                    0 competitors
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default ProductScraper; 