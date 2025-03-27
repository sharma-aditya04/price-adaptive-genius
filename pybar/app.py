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
        "Referer": "https://www.amazon.in/",
        "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        "sec-ch-ua-mobile": "?0",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1"
    }

def get_amazon_cookies(session):
    try:
        # Visit homepage first
        response = session.get("https://www.amazon.in", headers=get_random_headers())
        response.raise_for_status()
        
        # Get the necessary cookies
        cookies = session.cookies.get_dict()
        
        # Add additional cookies that Amazon expects
        cookies.update({
            "session-token": str(random.randint(1000000, 9999999)),
            "ubid-main": str(random.randint(1000000, 9999999)),
            "x-main": str(random.randint(1000000, 9999999))
        })
        
        return cookies
    except Exception as e:
        print(f"Failed to get cookies: {e}")
        return None

def scrape_amazon_product(url):
    time.sleep(random.uniform(2, 4))  # Increased delay
    headers = get_random_headers()
    
    try:
        session = requests.Session()
        
        # Get cookies first
        cookies = get_amazon_cookies(session)
        if not cookies:
            return {"error": "Failed to initialize session"}
        
        # Update session cookies
        session.cookies.update(cookies)
        
        # Add a small delay before making the product request
        time.sleep(random.uniform(1, 2))
        
        # Make the product request
        response = session.get(url, headers=headers)
        response.raise_for_status()
        
        if "Sorry, we just need to make sure you're not a robot" in response.text or "Enter the characters you see below" in response.text:
            return {"error": "CAPTCHA detected. Please try again later."}
            
    except requests.RequestException as e:
        print(f"Failed to fetch the webpage: {e}")
        return None
    
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
    
    # Extract additional product details
    details = {}
    
    # Extract product description
    description = None
    desc_selectors = [
        "div#productDescription",
        "div#productDescription p",
        "div#productDescription span",
        "div#productDescription div",
        "div#productDescription ul",
        "div#productDescription li"
    ]
    
    for selector in desc_selectors:
        desc_elem = soup.select_one(selector)
        if desc_elem:
            description = desc_elem.get_text(strip=True)
            break
    
    # Extract product features
    features = []
    feature_selectors = [
        "div#feature-bullets",
        "div#feature-bullets ul",
        "div#feature-bullets li",
        "div#feature-bullets span",
        "div#feature-bullets div"
    ]
    
    for selector in feature_selectors:
        feature_elem = soup.select_one(selector)
        if feature_elem:
            features = [item.get_text(strip=True) for item in feature_elem.find_all('li')]
            break
    
    # Extract product specifications
    specifications = {}
    spec_selectors = [
        "table#productOverview_feature_div",
        "table#productDetails_techSpec_section_1",
        "table#productDetails_detailBullets_sections1",
        "table#productDetails_detailBullets_sections2",
        "table#productDetails_detailBullets_sections3"
    ]
    
    for selector in spec_selectors:
        spec_table = soup.select_one(selector)
        if spec_table:
            rows = spec_table.find_all('tr')
            for row in rows:
                cols = row.find_all(['th', 'td'])
                if len(cols) == 2:
                    key = cols[0].get_text(strip=True)
                    value = cols[1].get_text(strip=True)
                    specifications[key] = value
    
    # Extract product rating
    rating = None
    rating_selectors = [
        "span.a-icon-alt",
        "div#averageCustomerReviews",
        "div#averageCustomerReviews span",
        "div#averageCustomerReviews i",
        "div#averageCustomerReviews div"
    ]
    
    for selector in rating_selectors:
        rating_elem = soup.select_one(selector)
        if rating_elem:
            rating = rating_elem.get_text(strip=True)
            break
    
    # Extract number of reviews
    reviews_count = None
    reviews_selectors = [
        "span#acrCustomerReviewText",
        "span#acrCustomerReviewText span",
        "span#acrCustomerReviewText div",
        "div#averageCustomerReviews span#acrCustomerReviewText"
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
    if not 'amazon.in' in url:
        return jsonify({"error": "URL must be from amazon.in"}), 400
    
    product_info = scrape_amazon_product(url)
    if not product_info:
        return jsonify({"error": "Failed to scrape the product"}), 500
    
    if "error" in product_info:
        return jsonify(product_info), 400
    
    return jsonify(product_info)

if __name__ == '__main__':
    app.run(debug=True, port=5000)