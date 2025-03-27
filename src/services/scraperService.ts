import axios from 'axios';

interface ProductInfo {
  "Product Name": string;
  "Price": string;
  "Stock": string;
  "Image URL": string;
  "Image": string;
}

interface ScraperResponse {
  data: ProductInfo;
  error?: string;
}

const SCRAPER_PORTS = {
  amazon: 5000,
  flipkart: 5001,
  myntra: 5002,
  ajio: 5003
};

const detectSite = (url: string): string | null => {
  if (url.includes('amazon.com') || url.includes('amazon.in')) return 'amazon';
  if (url.includes('flipkart.com')) return 'flipkart';
  if (url.includes('myntra.com')) return 'myntra';
  if (url.includes('ajio.com')) return 'ajio';
  return null;
};

export const scrapeProduct = async (url: string): Promise<ScraperResponse> => {
  try {
    const site = detectSite(url);
    if (!site) {
      return {
        data: {
          "Product Name": "N/A",
          "Price": "N/A",
          "Stock": "N/A",
          "Image URL": "",
          "Image": "Unsupported website"
        },
        error: "Unsupported website. Please use Amazon, Flipkart, Myntra, or AJIO URLs."
      };
    }

    const port = SCRAPER_PORTS[site as keyof typeof SCRAPER_PORTS];
    const response = await axios.post(`http://localhost:${port}/scrape`, { url });
    return { data: response.data };
  } catch (error: any) {
    return {
      data: {
        "Product Name": "N/A",
        "Price": "N/A",
        "Stock": "N/A",
        "Image URL": "",
        "Image": "Failed to scrape"
      },
      error: error.response?.data?.error || "Failed to scrape the product"
    };
  }
}; 