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

app = Flask(__name__)
CORS(app)

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
        "Cache-Control": "max-age=0",
        "Referer": "https://www.pantaloons.com/",
        "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        "sec-ch-ua-mobile": "?0",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1"
    }

def scrape_pantaloons_product(url):
    time.sleep(random.uniform(2, 4))  # Random delay to avoid rate limiting
    headers = get_random_headers()
    
    try:
        session = requests.Session()
        
        # Add a small delay before making the request
        time.sleep(random.uniform(1, 2))
        
        # Make the product request
        response = session.get(url, headers=headers)
        response.raise_for_status()
        
        if "Access Denied" in response.text or "Bot detected" in response.text:
            return {"error": "Access denied. Please try again later."}
            
    except requests.RequestException as e:
        print(f"Failed to fetch the webpage: {e}")
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract product name - Pantaloons specific selectors
    product_name = None
    name_selectors = [
        "h1.product-title",
        "h1.product-name",
        "h1[class*='product-title']",
        "h1[class*='product-name']",
        "div.product-title h1",
        "div.product-name h1"
    ]
    
    for selector in name_selectors:
        product_name = soup.select_one(selector)
        if product_name:
            product_name = product_name.get_text(strip=True)
            break
    
    # Extract price - Pantaloons specific selectors
    price = None
    price_selectors = [
        "span.price",
        "span.product-price",
        "div.price span",
        "div.product-price span",
        "span[class*='price']",
        "span[class*='product-price']"
    ]
    
    for selector in price_selectors:
        price_elem = soup.select_one(selector)
        if price_elem:
            price = clean_price(price_elem.get_text())
            break
    
    # Extract stock availability - Pantaloons specific selectors
    stock = None
    stock_selectors = [
        "div.stock-status",
        "div.availability",
        "span.stock-status",
        "span.availability",
        "div[class*='stock']",
        "div[class*='availability']"
    ]
    
    for selector in stock_selectors:
        stock_elem = soup.select_one(selector)
        if stock_elem:
            stock = stock_elem.get_text(strip=True)
            break
    
    # Extract product image - Pantaloons specific selectors
    image_url = None
    image_selectors = [
        "img.product-image",
        "img.main-image",
        "div.product-image img",
        "div.main-image img",
        "img[class*='product-image']",
        "img[class*='main-image']"
    ]
    
    for selector in image_selectors:
        image_tag = soup.select_one(selector)
        if image_tag and 'src' in image_tag.attrs:
            image_url = image_tag['src']
            if not image_url.startswith('http'):
                image_url = 'https:' + image_url
            break
    
    # Extract additional product details
    details = {}
    
    # Extract product description
    description = None
    desc_selectors = [
        "div.product-description",
        "div.description",
        "div[class*='product-description']",
        "div[class*='description']"
    ]
    
    for selector in desc_selectors:
        desc_elem = soup.select_one(selector)
        if desc_elem:
            description = desc_elem.get_text(strip=True)
            break
    
    # Extract product features
    features = []
    feature_selectors = [
        "div.product-features",
        "div.features",
        "ul.features-list",
        "div[class*='product-features']",
        "div[class*='features']"
    ]
    
    for selector in feature_selectors:
        feature_elem = soup.select_one(selector)
        if feature_elem:
            features = [item.get_text(strip=True) for item in feature_elem.find_all('li')]
            break
    
    # Extract product specifications
    specifications = {}
    spec_selectors = [
        "div.product-specifications",
        "div.specifications",
        "table.specifications-table",
        "div[class*='product-specifications']",
        "div[class*='specifications']"
    ]
    
    for selector in spec_selectors:
        spec_table = soup.select_one(selector)
        if spec_table:
            rows = spec_table.find_all(['tr', 'div'])
            for row in rows:
                cols = row.find_all(['th', 'td', 'div'])
                if len(cols) == 2:
                    key = cols[0].get_text(strip=True)
                    value = cols[1].get_text(strip=True)
                    specifications[key] = value
    
    # Extract product rating
    rating = None
    rating_selectors = [
        "div.product-rating",
        "div.rating",
        "span.rating",
        "div[class*='product-rating']",
        "div[class*='rating']"
    ]
    
    for selector in rating_selectors:
        rating_elem = soup.select_one(selector)
        if rating_elem:
            rating = rating_elem.get_text(strip=True)
            break
    
    # Extract number of reviews
    reviews_count = None
    reviews_selectors = [
        "div.review-count",
        "span.review-count",
        "div[class*='review-count']",
        "span[class*='review-count']"
    ]
    
    for selector in reviews_selectors:
        reviews_elem = soup.select_one(selector)
        if reviews_elem:
            reviews_count = reviews_elem.get_text(strip=True)
            break
    
    product_info = {
        "Product Name": product_name or "N/A",
        "Price": price or "N/A",
        "Stock": stock or "N/A",
        "Image URL": image_url,
        "Description": description or "N/A",
        "Features": features or [],
        "Specifications": specifications or {},
        "Rating": rating or "N/A",
        "Reviews Count": reviews_count or "N/A"
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
    if not ('pantaloons.com' in url or 'www.pantaloons.com' in url):
        return jsonify({"error": "URL must be from pantaloons.com"}), 400
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    product_info = scrape_pantaloons_product(url)
    if not product_info:
        return jsonify({"error": "Failed to scrape the product"}), 500
    
    if "error" in product_info:
        return jsonify(product_info), 400
    
    return jsonify(product_info)

if __name__ == '__main__':
    app.run(debug=True, port=5004) 