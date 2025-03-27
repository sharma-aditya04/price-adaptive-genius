import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import time
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def clean_price(price_text):
    if not price_text:
        return "N/A"
    # Remove any non-numeric characters except decimal point
    price = re.sub(r'[^\d.]', '', price_text)
    return price if price else "N/A"

def get_random_headers():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15"
    ]
    
    return {
        "User-Agent": random.choice(user_agents),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0"
    }

def scrape_amazon_product(url):
    # Add a random delay to avoid rate limiting
    time.sleep(random.uniform(1, 3))
    
    headers = get_random_headers()
    
    try:
        session = requests.Session()
        response = session.get(url, headers=headers)
        response.raise_for_status()
        
        # Check if we hit a CAPTCHA page
        if "Type the characters you see in this image" in response.text:
            return {"error": "CAPTCHA detected. Please try again later."}
            
    except requests.RequestException as e:
        print(f"Failed to fetch the webpage: {e}")
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract product name - try multiple selectors
    product_name = None
    name_selectors = [
        "#productTitle",
        "#title",
        "h1.a-size-large",
        "h1.a-size-medium",
        "h1.a-text-normal",
        "span.a-size-large.product-title-word-break",
        "span.a-size-large.a-color-base"
    ]
    
    for selector in name_selectors:
        product_name = soup.select_one(selector)
        if product_name:
            product_name = product_name.get_text(strip=True)
            break
    
    # Extract price - try multiple selectors
    price = None
    price_selectors = [
        "span.a-price-whole",
        "span.a-price span.a-offscreen",
        "span.a-price",
        "span.a-text-price",
        "span.a-color-price",
        "span.a-price.a-text-price",
        "span.a-price.aok-align-center",
        "span.a-price.aok-align-center span.a-offscreen"
    ]
    
    for selector in price_selectors:
        price_elem = soup.select_one(selector)
        if price_elem:
            price = clean_price(price_elem.get_text())
            break
    
    # Extract stock availability - try multiple selectors
    stock = None
    stock_selectors = [
        "#availability",
        "#availability span",
        "div#deliveryMessageMirId",
        "div.a-section.a-spacing-none.a-spacing-top-micro",
        "div.a-section.a-spacing-none.a-spacing-top-mini",
        "div.a-section.a-spacing-none.a-spacing-top-small"
    ]
    
    for selector in stock_selectors:
        stock_elem = soup.select_one(selector)
        if stock_elem:
            stock = stock_elem.get_text(strip=True)
            break
    
    # Extract product image - try multiple selectors
    image_url = None
    image_selectors = [
        "#landingImage",
        "#imgBlkFront",
        "#main-image",
        "img.a-dynamic-image",
        "img#landingImage",
        "img#imgBlkFront",
        "img#main-image"
    ]
    
    for selector in image_selectors:
        image_tag = soup.select_one(selector)
        if image_tag and 'src' in image_tag.attrs:
            image_url = image_tag['src']
            break
    
    product_info = {
        "Product Name": product_name or "N/A",
        "Price": price or "N/A",
        "Stock": stock or "N/A",
        "Image URL": image_url
    }
    
    if image_url:
        try:
            image_response = session.get(image_url, headers=headers)
            img = Image.open(BytesIO(image_response.content))
            product_info["Image"] = "Image loaded successfully"
        except Exception as e:
            product_info["Image"] = f"Failed to load image: {e}"
    
    return product_info

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "URL is required"}), 400
    
    url = data['url']
    if not ('amazon.com' in url or 'amazon.in' in url):
        return jsonify({"error": "URL must be from amazon.com or amazon.in"}), 400
    
    product_info = scrape_amazon_product(url)
    if not product_info:
        return jsonify({"error": "Failed to scrape the product"}), 500
    
    if "error" in product_info:
        return jsonify(product_info), 400
    
    return jsonify(product_info)

if __name__ == '__main__':
    app.run(debug=True)