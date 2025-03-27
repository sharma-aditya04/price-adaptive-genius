export interface ProductInfo {
  "Product Name": string;
  "Price": string;
  "Stock": string;
  "Image URL": string;
  "Description"?: string;
  "Features"?: string[];
  "Specifications"?: Record<string, string>;
  "Rating"?: string;
  "Reviews Count"?: string;
}

export const scrapeProduct = async (url: string): Promise<ProductInfo> => {
  try {
    let endpoint = '';
    
    // Clean and validate URL
    url = url.trim();
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
      url = 'https://' + url;
    }
    
    console.log('Processing URL:', url); // Debug log
    
    // Determine which scraper to use based on the URL
    if (url.includes('amazon.in')) {
      endpoint = 'http://localhost:5000/scrape';
    } else if (url.includes('flipkart.com')) {
      endpoint = 'http://localhost:5001/scrape';
    } else if (url.includes('myntra.com')) {
      endpoint = 'http://localhost:5002/scrape';
    } else if (url.includes('ajio.com')) {
      endpoint = 'http://localhost:5003/scrape';
    } else if (url.includes('pantaloons.com')) {
      console.log('Using Pantaloons scraper'); // Debug log
      endpoint = 'http://localhost:5004/scrape';
    } else if (url.includes('nike.com/in') || url.includes('nike.in')) {
      console.log('Using Nike scraper'); // Debug log
      endpoint = 'http://localhost:5005/scrape';
    } else {
      console.log('No matching scraper found for URL'); // Debug log
      throw new Error('Unsupported website. Please use a valid URL from Amazon, Flipkart, Myntra, AJIO, Pantaloons, or Nike India.');
    }

    console.log('Using endpoint:', endpoint); // Debug log

    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url }),
    });

    if (!response.ok) {
      const error = await response.json();
      console.error('Server error:', error); // Debug log
      throw new Error(error.error || `Failed to scrape product. Server returned ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error: any) {
    console.error('Error details:', {
      message: error.message,
      stack: error.stack,
      url: url
    });
    throw error;
  }
}; 