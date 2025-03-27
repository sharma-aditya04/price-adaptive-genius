import axios from 'axios';

interface AmazonProductInfo {
  "Product Name": string;
  "Price": string;
  "Stock": string;
  "Image URL": string;
  "Image": string;
}

export const scrapeAmazonProduct = async (url: string): Promise<AmazonProductInfo> => {
  try {
    const response = await axios.post('http://localhost:5000/scrape', { url });
    return response.data;
  } catch (error) {
    console.error('Error scraping Amazon product:', error);
    throw error;
  }
}; 