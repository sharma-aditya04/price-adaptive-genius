import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import time
import random
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure CORS
CORS(app, resources={
    r"/*": {
        "origins": ["*"],  # Allow all origins
        "methods": ["POST", "GET", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Load dummy products
try:
    with open('dummy_products.json', 'r') as f:
        dummy_products = json.load(f)
except FileNotFoundError:
    dummy_products = []

def clean_price(price_text):
    if not price_text:
        return "N/A"
    # Remove any non-numeric characters except decimal point
    price = re.sub(r'[^\d.]', '', price_text)
    return price if price else "N/A"

def get_random_headers():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Firefox/122.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Edge/120.0.0.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ]
    
    return {
        "User-Agent": random.choice(user_agents),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "pragma": "no-cache",
        "cache-control": "no-cache",
        "dnt": "1"
    }

def get_amazon_cookies(session):
    try:
        # First visit Amazon homepage to get initial cookies
        homepage_url = "https://www.amazon.in"
        headers = get_random_headers()
        
        # Add random delay before request
        time.sleep(random.uniform(0.5, 1))  # Reduced delay for serverless
        
        response = session.get(homepage_url, headers=headers)
        response.raise_for_status()
        
        # Get cookies from the response
        cookies = session.cookies.get_dict()
        
        # Add common Amazon cookies
        additional_cookies = {
            "session-id": str(random.randint(100000000, 999999999)),
            "session-id-time": str(int(time.time())),
            "i18n-prefs": "INR",
            "lc-acbin": "en_IN",
            "sp-cdn": "L5Z9:IN",
            "ubid-acbin": f"257-{random.randint(1000000, 9999999)}-{random.randint(1000000, 9999999)}",
            "session-token": ''.join(random.choices('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', k=248))
        }
        
        cookies.update(additional_cookies)
        return cookies
        
    except Exception as e:
        print(f"Error getting cookies: {e}")
        return None

def scrape_amazon_product(url):
    try:
        # Add headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }

        # Add a delay to avoid rate limiting
        time.sleep(random.uniform(1, 3))

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract product details with more robust selectors
        title = soup.select_one('#productTitle')
        price = soup.select_one('.a-price-whole')
        original_price = soup.select_one('.a-price.a-text-price .a-offscreen')
        image = soup.select_one('#landingImage')
        description = soup.select_one('#productDescription')
        brand = soup.select_one('#bylineInfo')
        category = soup.select_one('#wayfinding-breadcrumbs_container')
        
        # Clean and format the extracted data
        product_data = {
            'name': title.text.strip() if title else 'N/A',
            'current_price': float(clean_price(price.text)) if price else 0.0,
            'base_price': float(clean_price(original_price.text)) if original_price else 0.0,
            'url': image.get('src') if image else '',
            'description': description.text.strip() if description else 'N/A',
            'brand': brand.text.strip().replace('Brand: ', '') if brand else 'N/A',
            'category': extract_category(category.text.strip()) if category else 'Uncategorized',
            'subcategory': extract_subcategory(category.text.strip()) if category else 'Uncategorized'
        }
        
        return product_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching product: {str(e)}")
        return None
    except Exception as e:
        print(f"Error processing product: {str(e)}")
        return None

def extract_category(breadcrumb_text):
    try:
        # Split the breadcrumb text and get the main category
        categories = [cat.strip() for cat in breadcrumb_text.split('›')]
        return categories[0] if categories else 'Uncategorized'
    except:
        return 'Uncategorized'

def extract_subcategory(breadcrumb_text):
    try:
        # Split the breadcrumb text and get the subcategory
        categories = [cat.strip() for cat in breadcrumb_text.split('›')]
        return categories[1] if len(categories) > 1 else 'Uncategorized'
    except:
        return 'Uncategorized'

def scrape_flipkart_product(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }

        time.sleep(random.uniform(1, 3))
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Flipkart specific selectors
        title = soup.select_one('.B_NuCI')
        price = soup.select_one('._30jeq3._16Jk6d')
        original_price = soup.select_one('._3I9_wc._2p6lqe')
        image = soup.select_one('._396cs4._2amPTt._3qGmMb')
        description = soup.select_one('._1AN87F')
        brand = soup.select_one('._2WkVRV')
        category = soup.select_one('._2whKao')
        
        product_data = {
            'name': title.text.strip() if title else 'N/A',
            'current_price': float(clean_price(price.text)) if price else 0.0,
            'base_price': float(clean_price(original_price.text)) if original_price else 0.0,
            'url': image.get('src') if image else '',
            'description': description.text.strip() if description else 'N/A',
            'brand': brand.text.strip() if brand else 'N/A',
            'category': extract_category(category.text.strip()) if category else 'Uncategorized',
            'subcategory': extract_subcategory(category.text.strip()) if category else 'Uncategorized'
        }
        
        return product_data
    except Exception as e:
        print(f"Error scraping Flipkart product: {str(e)}")
        return None

@app.route('/api/scrape', methods=['POST'])
def scrape_product():
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({"error": "URL is required"}), 400
            
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        # Clean the URL by removing tracking parameters
        clean_url = re.sub(r'[?&](ref_|tag_|linkCode|pd_rd_|pf_rd_|content-id|encoding).*?(?=[&]|$)', '', url)
        
        # Determine which scraper to use based on the URL
        if 'amazon.in' in clean_url:
            product_data = scrape_amazon_product(clean_url)
        elif 'flipkart.com' in clean_url:
            product_data = scrape_flipkart_product(clean_url)
        else:
            return jsonify({"error": "Only Amazon.in and Flipkart.com URLs are supported"}), 400
        
        if not product_data:
            return jsonify({"error": "Failed to scrape product data"}), 500
            
        return jsonify(product_data), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        # Get query parameters
        category = request.args.get('category')
        subcategory = request.args.get('subcategory')
        brand = request.args.get('brand')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        
        # Filter products based on query parameters
        filtered_products = dummy_products
        
        if category:
            filtered_products = [p for p in filtered_products if p['category'] == category]
        
        if subcategory:
            filtered_products = [p for p in filtered_products if p['subcategory'] == subcategory]
        
        if brand:
            filtered_products = [p for p in filtered_products if p['brand'] == brand]
        
        if min_price is not None:
            filtered_products = [p for p in filtered_products if p['current_price'] >= min_price]
        
        if max_price is not None:
            filtered_products = [p for p in filtered_products if p['current_price'] <= max_price]
        
        return jsonify({
            "total": len(filtered_products),
            "products": filtered_products
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/products/categories', methods=['GET'])
def get_categories():
    try:
        categories = {}
        for product in dummy_products:
            if product['category'] not in categories:
                categories[product['category']] = set()
            categories[product['category']].add(product['subcategory'])
        
        # Convert sets to lists for JSON serialization
        categories = {k: list(v) for k, v in categories.items()}
        return jsonify(categories)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/products/brands', methods=['GET'])
def get_brands():
    try:
        brands = set()
        for product in dummy_products:
            brands.add(product['brand'])
        return jsonify(list(brands))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# For local development
if __name__ == '__main__':
    app.run(debug=True, port=5000)