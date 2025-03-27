
import React, { useState } from 'react';
import Navbar from '../components/Navbar';
import DashboardHeader from '../components/DashboardHeader';
import ProductCard from '../components/ProductCard';
import PriceComparison from '../components/PriceComparison';
import PricingRules from '../components/PricingRules';
import PriceChart from '../components/PriceChart';
import { Product as SupabaseProduct } from '../types/supabase';
import { products as mockProducts, categories, Product as MockProduct } from '../data/mockData';
import { toast } from "sonner";

// Helper function to convert MockProduct to SupabaseProduct
const convertMockToSupabaseProduct = (mockProduct: MockProduct): SupabaseProduct => {
  return {
    id: mockProduct.id.toString(),
    name: mockProduct.name,
    current_price: mockProduct.currentPrice,
    previous_price: mockProduct.previousPrice,
    suggested_price: mockProduct.suggestedPrice,
    category: mockProduct.category,
    image_url: mockProduct.image,
    in_stock: mockProduct.inStock
  };
};

const Index = () => {
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [selectedProduct, setSelectedProduct] = useState<SupabaseProduct | null>(null);
  const [localProducts, setLocalProducts] = useState<MockProduct[]>(mockProducts);
  const [isFilterVisible, setIsFilterVisible] = useState(false);

  const filteredProducts = selectedCategory === 'All'
    ? localProducts
    : localProducts.filter(product => product.category === selectedCategory);

  const handleProductSelect = (product: MockProduct) => {
    setSelectedProduct(convertMockToSupabaseProduct(product));
    // Scroll to top on mobile when product is selected
    if (window.innerWidth < 768) {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const handleApplyRules = (productId: string, rules: string[], newPrice: number) => {
    // Update the product price
    const updatedProducts = localProducts.map(product => {
      if (product.id.toString() === productId) {
        const updatedProduct = {
          ...product,
          previousPrice: product.currentPrice,
          currentPrice: newPrice
        };
        setSelectedProduct(convertMockToSupabaseProduct(updatedProduct));
        return updatedProduct;
      }
      return product;
    });
    
    setLocalProducts(updatedProducts);
    
    // Show toast message
    toast.success("Price updated successfully", {
      description: `New price: $${newPrice.toFixed(2)}`,
      position: "bottom-right",
    });
  };

  const handleRefresh = () => {
    toast.info("Refreshing pricing data...", {
      position: "bottom-right",
    });
    
    // Simulate a refresh by waiting 1 second
    setTimeout(() => {
      toast.success("Pricing data updated", {
        description: "Latest market data has been loaded",
        position: "bottom-right",
      });
    }, 1000);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <div className="pt-16 pb-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="pt-8">
            <DashboardHeader 
              title="Dynamic Pricing Dashboard" 
              subtitle="Optimize your prices based on real-time market data and AI recommendations"
              onRefresh={handleRefresh}
              onFilterToggle={() => setIsFilterVisible(!isFilterVisible)}
            />
            
            {isFilterVisible && (
              <div className="mb-6 p-4 bg-white rounded-lg border border-gray-200 animate-fade-in-fast">
                <h3 className="font-medium text-gray-900 mb-3">Filter Products</h3>
                <div className="flex flex-wrap gap-2">
                  {categories.map(category => (
                    <button
                      key={category}
                      onClick={() => setSelectedCategory(category)}
                      className={`px-3 py-1 rounded-full text-sm transition-colors ${
                        selectedCategory === category
                          ? 'bg-gray-900 text-white'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      {category}
                    </button>
                  ))}
                </div>
              </div>
            )}

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Product listing */}
              <div className="lg:col-span-2">
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-3 gap-4">
                  {filteredProducts.map(product => (
                    <ProductCard 
                      key={product.id} 
                      product={product} 
                      onClick={handleProductSelect} 
                    />
                  ))}
                </div>
                
                {filteredProducts.length === 0 && (
                  <div className="bg-white p-8 rounded-lg border border-gray-200 flex flex-col items-center justify-center text-center">
                    <p className="text-gray-600 mb-4">No products found in this category</p>
                    <button
                      onClick={() => setSelectedCategory('All')}
                      className="px-4 py-2 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 transition-colors"
                    >
                      Show all products
                    </button>
                  </div>
                )}
              </div>
              
              {/* Product details and controls */}
              <div className="space-y-6">
                {selectedProduct ? (
                  <>
                    <PriceComparison product={selectedProduct} />
                    <PriceChart product={selectedProduct} />
                    <PricingRules 
                      product={selectedProduct} 
                      onApplyRules={handleApplyRules} 
                    />
                  </>
                ) : (
                  <div className="bg-white p-8 rounded-lg border border-gray-200 text-center">
                    <p className="text-gray-600 mb-2">Select a product to view details</p>
                    <p className="text-gray-500 text-sm">
                      You'll be able to compare prices and apply custom pricing rules
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Index;
