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
    max_retries = 1  # Reduced retries for serverless
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            session = requests.Session()
            
            # Get cookies first
            cookies = get_amazon_cookies(session)
            if not cookies:
                return {"error": "Failed to initialize session"}
            
            # Update session cookies
            session.cookies.update(cookies)
            
            # Clean the URL by removing tracking parameters
            clean_url = url.split('/ref=')[0].split('?')[0]
            
            # Make the product request
            headers = get_random_headers()
            response = session.get(clean_url, headers=headers, cookies=cookies)
            response.raise_for_status()
            
            # Check for CAPTCHA or bot detection
            if any(text in response.text.lower() for text in [
                "sorry, we just need to make sure you're not a robot",
                "enter the characters you see below",
                "bot check",
                "automatic bot",
                "security check",
                "captcha"
            ]):
                return {"error": "Amazon's anti-bot protection is active. Please try again later."}
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract product name - Amazon specific selectors
            product_name = None
            name_selectors = [
                "h1.product-title",
                "h1.product-title-word-break",
                "h1.a-size-large",
                "h1.a-size-large.product-title-word-break",
                "h1.a-text-normal",
                "h1.a-text-normal.product-title-word-break",
                "h1[class*='product-title']",
                "h1[class*='product-title-word-break']",
                "h1[class*='a-size-large']",
                "h1[class*='a-text-normal']"
            ]
            
            for selector in name_selectors:
                product_name = soup.select_one(selector)
                if product_name:
                    product_name = product_name.get_text(strip=True)
                    break
            
            # Extract price - Amazon specific selectors
            price = None
            price_selectors = [
                "span.a-price-whole",
                "span.a-price",
                "span.a-text-price",
                "span.a-offscreen",
                "span.a-price span.a-offscreen",
                "div.a-price span.a-offscreen",
                "div.a-price-whole",
                "div.a-price span.a-text-price",
                "div.a-price span.a-offscreen",
                "div.a-price-whole span.a-offscreen"
            ]
            
            for selector in price_selectors:
                price_elem = soup.select_one(selector)
                if price_elem:
                    price = clean_price(price_elem.get_text())
                    break
            
            # Extract stock availability - Amazon specific selectors
            stock = None
            stock_selectors = [
                "div#availability",
                "div#availability span",
                "div#availability span.a-color-price",
                "div#availability span.a-color-success",
                "div#availability span.a-color-error",
                "div#availability span.a-color-warning",
                "div#availability span.a-text-bold",
                "div#availability span.a-text-success",
                "div#availability span.a-text-error",
                "div#availability span.a-text-warning"
            ]
            
            for selector in stock_selectors:
                stock_elem = soup.select_one(selector)
                if stock_elem:
                    stock = stock_elem.get_text(strip=True)
                    break
            
            # Extract product image - Amazon specific selectors
            image_url = None
            image_selectors = [
                "img#landingImage",
                "img#imgBlkFront",
                "img#main-image",
                "img#main-image-default",
                "img#main-image-default-0",
                "img#main-image-default-1",
                "img#main-image-default-2",
                "img#main-image-default-3",
                "img#main-image-default-4",
                "img#main-image-default-5"
            ]
            
            for selector in image_selectors:
                image_tag = soup.select_one(selector)
                if image_tag and 'src' in image_tag.attrs:
                    image_url = image_tag['src']
                    if not image_url.startswith('http'):
                        image_url = 'https:' + image_url
                    break
            
            product_info = {
                "Product Name": product_name or "N/A",
                "Price": price or "N/A",
                "Stock": stock or "N/A",
                "Image URL": image_url
            }
            
            return product_info
            
        except requests.RequestException as e:
            print(f"Failed to fetch the webpage: {e}")
            return {"error": "Failed to access Amazon. Please try again later."}
        except Exception as e:
            print(f"Unexpected error: {e}")
            return {"error": "An unexpected error occurred while scraping the product."}

@app.route('/api/scrape', methods=['POST'])
def scrape():
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({"error": "URL is required"}), 400
        
        url = data['url']
        if not 'amazon.in' in url:
            return jsonify({"error": "URL must be from amazon.in"}), 400
        
        product_info = scrape_amazon_product(url)
        if not product_info:
            return jsonify({"error": "Failed to scrape the product"}), 500
        
        if "error" in product_info:
            return jsonify(product_info), 400
        
        return jsonify(product_info)
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