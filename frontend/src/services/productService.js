import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

export const productService = {
    // Scrape product data from URL
    scrapeProduct: async (url) => {
        try {
            const response = await axios.post(`${API_BASE_URL}/scrape`, { url });
            return response.data;
        } catch (error) {
            console.error('Error scraping product:', error);
            throw new Error(error.response?.data?.error || 'Failed to scrape product data');
        }
    },

    // Get all products with optional filters
    getProducts: async (filters = {}) => {
        try {
            const params = new URLSearchParams();
            if (filters.category) params.append('category', filters.category);
            if (filters.subcategory) params.append('subcategory', filters.subcategory);
            if (filters.brand) params.append('brand', filters.brand);
            if (filters.minPrice) params.append('min_price', filters.minPrice);
            if (filters.maxPrice) params.append('max_price', filters.maxPrice);

            const response = await axios.get(`${API_BASE_URL}/products?${params.toString()}`);
            return response.data;
        } catch (error) {
            console.error('Error fetching products:', error);
            throw error;
        }
    },

    // Get all categories and their subcategories
    getCategories: async () => {
        try {
            const response = await axios.get(`${API_BASE_URL}/products/categories`);
            return response.data;
        } catch (error) {
            console.error('Error fetching categories:', error);
            throw error;
        }
    },

    // Get all unique brands
    getBrands: async () => {
        try {
            const response = await axios.get(`${API_BASE_URL}/products/brands`);
            return response.data;
        } catch (error) {
            console.error('Error fetching brands:', error);
            throw error;
        }
    }
}; 