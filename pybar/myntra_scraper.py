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
        "Referer": "https://www.myntra.com/",
        "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        "sec-ch-ua-mobile": "?0",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "x-requested-with": "XMLHttpRequest",
        "x-request-id": str(random.randint(1000000, 9999999)),
        "x-request-timestamp": str(int(time.time() * 1000))
    }

def get_myntra_cookies(session):
    try:
        # Visit homepage first
        response = session.get("https://www.myntra.com", headers=get_random_headers())
        response.raise_for_status()
        
        # Get the necessary cookies
        cookies = session.cookies.get_dict()
        
        # Add additional cookies that Myntra expects
        cookies.update({
            "myntraWeb": "true",
            "myntraWebVersion": "1.0",
            "myntraWebPlatform": "web",
            "myntraWebDevice": "desktop",
            "myntraWebBrowser": "chrome",
            "myntraWebOS": "windows"
        })
        
        return cookies
    except Exception as e:
        print(f"Failed to get cookies: {e}")
        return None

def scrape_myntra_product(url):
    time.sleep(random.uniform(2, 4))  # Increased delay
    headers = get_random_headers()
    
    try:
        session = requests.Session()
        
        # Get cookies first
        cookies = get_myntra_cookies(session)
        if not cookies:
            return {"error": "Failed to initialize session"}
        
        # Update session cookies
        session.cookies.update(cookies)
        
        # Add a small delay before making the product request
        time.sleep(random.uniform(1, 2))
        
        # Make the product request
        response = session.get(url, headers=headers)
        response.raise_for_status()
        
        if "Oops! Something went wrong" in response.text or "Please verify you are a human" in response.text:
            return {"error": "Access denied. Please try again later."}
            
    except requests.RequestException as e:
        print(f"Failed to fetch the webpage: {e}")
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract product name - Myntra specific selectors
    product_name = None
    name_selectors = [
        "h1.pdp-name",
        "h1.pdp-title",
        "h1.pdp-product-name",
        "div.pdp-name",
        "div.pdp-title",
        "h1[class*='product-name']",
        "h1[class*='product-title']",
        "div[class*='product-name']",
        "div[class*='product-title']",
        "span[class*='product-name']",
        "span[class*='product-title']",
        "h1[class*='pdp-name']",
        "h1[class*='pdp-title']"
    ]
    
    for selector in name_selectors:
        product_name = soup.select_one(selector)
        if product_name:
            product_name = product_name.get_text(strip=True)
            break
    
    # Extract price - Myntra specific selectors
    price = None
    price_selectors = [
        "span.pdp-price",
        "div.pdp-price",
        "span.pdp-product-price",
        "div.pdp-product-price",
        "span.pdp-price strong",
        "div[class*='price']",
        "span[class*='price']",
        "div[class*='product-price']",
        "span[class*='product-price']",
        "div[class*='selling-price']",
        "span[class*='selling-price']",
        "div[class*='pdp-price']",
        "span[class*='pdp-price']"
    ]
    
    for selector in price_selectors:
        price_elem = soup.select_one(selector)
        if price_elem:
            price = clean_price(price_elem.get_text())
            break
    
    # Extract stock availability - Myntra specific selectors
    stock = None
    stock_selectors = [
        "div.pdp-size-info",
        "div.pdp-size-description",
        "div.pdp-size-chart",
        "div.pdp-size-chart-info",
        "div.pdp-size-chart-description",
        "div[class*='size-info']",
        "div[class*='size-description']",
        "div[class*='stock-info']",
        "div[class*='availability']",
        "div[class*='delivery']",
        "div[class*='shipping']"
    ]
    
    for selector in stock_selectors:
        stock_elem = soup.select_one(selector)
        if stock_elem:
            stock = stock_elem.get_text(strip=True)
            break
    
    # Extract product image - Myntra specific selectors
    image_url = None
    image_selectors = [
        "img.pdp-image",
        "img.pdp-product-image",
        "div.pdp-image img",
        "div.pdp-product-image img",
        "div.pdp-image-container img",
        "img[class*='product-image']",
        "img[class*='product-img']",
        "img[class*='main-image']",
        "img[class*='primary-image']",
        "img[class*='gallery-image']",
        "img[class*='pdp-image']",
        "img[class*='pdp-product-image']"
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
    if not 'myntra.com' in url:
        return jsonify({"error": "URL must be from myntra.com"}), 400
    
    product_info = scrape_myntra_product(url)
    if not product_info:
        return jsonify({"error": "Failed to scrape the product"}), 500
    
    if "error" in product_info:
        return jsonify(product_info), 400
    
    return jsonify(product_info)

if __name__ == '__main__':
    app.run(debug=True, port=5002) 