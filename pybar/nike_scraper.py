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

def get_nike_cookies(session):
    try:
        # First visit Nike homepage to get initial cookies
        homepage_url = "https://www.nike.com/in"
        headers = get_random_headers()
        
        # Add random delay before request
        time.sleep(random.uniform(2, 4))
        
        response = session.get(homepage_url, headers=headers)
        response.raise_for_status()
        
        # Get cookies from the response
        cookies = session.cookies.get_dict()
        
        # Add common Nike cookies
        additional_cookies = {
            "CONSUMERCHOICE": "in/en_gb",
            "NIKE_COMMERCE_COUNTRY": "IN",
            "NIKE_COMMERCE_LANG_LOCALE": "en_GB",
            "currentSite": "nike.com",
            "guidU": ''.join(random.choices('0123456789abcdef', k=32)),
            "visitId": str(random.randint(1000000000, 9999999999)),
            "AnalysisUserId": ''.join(random.choices('0123456789abcdef', k=36))
        }
        
        cookies.update(additional_cookies)
        return cookies
        
    except Exception as e:
        print(f"Error getting cookies: {e}")
        return None

def scrape_nike_product(url):
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # Add random delay between retries
            if retry_count > 0:
                time.sleep(random.uniform(5, 10))
            
            session = requests.Session()
            
            # Get cookies first
            cookies = get_nike_cookies(session)
            if not cookies:
                return {"error": "Failed to initialize session"}
            
            # Update session cookies
            session.cookies.update(cookies)
            
            # Add random delay before product request
            time.sleep(random.uniform(3, 5))
            
            # Clean the URL by removing tracking parameters
            clean_url = url.split('?')[0]
            
            # Make the product request
            headers = get_random_headers()
            response = session.get(clean_url, headers=headers, cookies=cookies)
            response.raise_for_status()
            
            # Check for anti-bot measures with more specific Nike error messages
            if any(text in response.text.lower() for text in [
                "access denied",
                "security check",
                "captcha",
                "bot detected",
                "automated access",
                "please verify you are a human",
                "unusual traffic",
                "temporary hold",
                "we've detected unusual activity"
            ]):
                retry_count += 1
                if retry_count == max_retries:
                    return {
                        "error": "Nike's security system has detected automated access. Please try:\n" +
                                "1. Wait a few minutes before trying again\n" +
                                "2. Try a different Nike product\n" +
                                "3. Clear your browser cookies\n" +
                                "4. Use a different network connection"
                    }
                continue
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Enhanced product name selectors
            product_name = None
            name_selectors = [
                "h1.headline-2",
                "h1.product-title",
                "h1[data-test='product-title']",
                "div.product-info h1",
                "div.title h1",
                "h1#pdp_product_title",
                "h1.css-16cqcdq",
                "h1[data-auto-id='product-title']"
            ]
            
            for selector in name_selectors:
                product_name_elem = soup.select_one(selector)
                if product_name_elem:
                    product_name = product_name_elem.get_text(strip=True)
                    break
            
            # Enhanced price selectors with support for sale prices
            price = None
            sale_price = None
            price_selectors = [
                "div.product-price",
                "div[data-test='product-price']",
                "div.price-text",
                "div.product-info__price",
                "div.buying-price span",
                "div.css-b9fpep",
                "div[data-auto-id='product-price']",
                "span.css-1122yjz",
                "div.css-1122yjz"
            ]
            
            sale_price_selectors = [
                "div.sale-price",
                "div.css-12whm6j",
                "div[data-auto-id='sale-price']",
                "span.css-1122yjz.is-sale"
            ]
            
            # Check for sale price first
            for selector in sale_price_selectors:
                price_elem = soup.select_one(selector)
                if price_elem:
                    sale_price = clean_price(price_elem.get_text())
                    break
            
            # Then check regular price
            for selector in price_selectors:
                price_elem = soup.select_one(selector)
                if price_elem:
                    price = clean_price(price_elem.get_text())
                    break
            
            final_price = sale_price if sale_price else price
            
            # Enhanced stock availability with size information
            stock = None
            sizes_available = []
            stock_selectors = [
                "div.availability",
                "div[data-test='availability']",
                "div.stock-level",
                "div.product-status",
                "button.add-to-cart-btn",
                "div.buying-tools-container",
                "div[data-auto-id='size-selector']"
            ]
            
            size_selectors = [
                "div.size-grid button:not([disabled])",
                "div.css-1iv4hky button:not([disabled])",
                "div[data-auto-id='size-selector'] button:not([disabled])"
            ]
            
            # Check stock status
            for selector in stock_selectors:
                stock_elem = soup.select_one(selector)
                if stock_elem:
                    stock_text = stock_elem.get_text(strip=True).lower()
                    if any(text in stock_text for text in ["out of stock", "sold out", "notify me", "coming soon"]):
                        stock = "Out of Stock"
                    else:
                        stock = "In Stock"
                    break
            
            # Get available sizes
            for selector in size_selectors:
                size_elements = soup.select(selector)
                if size_elements:
                    sizes_available = [size.get_text(strip=True) for size in size_elements]
                    break
            
            # Enhanced image selectors with support for multiple images
            images = []
            image_selectors = [
                "img.product-image",
                "img[data-test='product-image']",
                "picture.hero-image img",
                "div.product-gallery img",
                "div.product-image img",
                "img.css-viwop1",
                "img[data-auto-id='product-image']",
                "div.css-1ju3qk7 img"
            ]
            
            for selector in image_selectors:
                image_tags = soup.select(selector)
                for tag in image_tags:
                    if 'src' in tag.attrs:
                        img_url = tag['src']
                        if not img_url.startswith('http'):
                            img_url = 'https:' + img_url
                        if img_url not in images:
                            images.append(img_url)
            
            # Enhanced description and features with better structure
            description = None
            desc_selectors = [
                "div.description-preview",
                "div[data-test='product-description']",
                "div.product-details",
                "div.product-info__description",
                "div.css-1pbvugw",
                "div[data-auto-id='product-description']"
            ]
            
            for selector in desc_selectors:
                desc_elem = soup.select_one(selector)
                if desc_elem:
                    description = desc_elem.get_text(strip=True)
                    break
            
            # Enhanced features with categories
            features = []
            benefits = []
            feature_selectors = [
                "div.description-preview ul li",
                "div.product-features li",
                "div.benefits-list li",
                "div[data-test='product-details'] li",
                "div.css-1pbvugw ul li",
                "div[data-auto-id='product-features'] li"
            ]
            
            benefit_selectors = [
                "div.benefits ul li",
                "div[data-auto-id='product-benefits'] li",
                "div.css-1pbvugw h3:contains('Benefits') + ul li"
            ]
            
            for selector in feature_selectors:
                feature_elems = soup.select(selector)
                if feature_elems:
                    features = [item.get_text(strip=True) for item in feature_elems]
                    break
            
            for selector in benefit_selectors:
                benefit_elems = soup.select(selector)
                if benefit_elems:
                    benefits = [item.get_text(strip=True) for item in benefit_elems]
                    break
            
            # Enhanced specifications with more details
            specifications = {}
            spec_selectors = [
                "div.product-details__information",
                "div.specifications",
                "div.product-info__specs",
                "div.css-1pbvugw",
                "div[data-auto-id='product-specifications']"
            ]
            
            spec_patterns = [
                (r'Style:|Style Code:', 'Style Code'),
                (r'Colour:|Color Shown:', 'Color'),
                (r'Country/Region of Origin:', 'Origin'),
                (r'Material:', 'Material'),
                (r'Shown:', 'Color Shown'),
                (r'Collection:', 'Collection'),
                (r'Category:', 'Category'),
                (r'Fit:', 'Fit'),
                (r'Last:', 'Last')
            ]
            
            for selector in spec_selectors:
                spec_elem = soup.select_one(selector)
                if spec_elem:
                    for pattern, key in spec_patterns:
                        value_elem = spec_elem.find(string=re.compile(pattern, re.I))
                        if value_elem:
                            specifications[key] = value_elem.find_next(text=True).strip()
                    break
            
            # Get color variants if available
            color_variants = []
            variant_selectors = [
                "div.color-chips button",
                "div[data-auto-id='color-picker'] button",
                "div.css-1iv4hky button[data-color]"
            ]
            
            for selector in variant_selectors:
                variant_elems = soup.select(selector)
                if variant_elems:
                    for elem in variant_elems:
                        color_name = elem.get('aria-label', '').replace('Select Color ', '')
                        color_url = elem.get('data-url', '')
                        if color_name and color_url:
                            if not color_url.startswith('http'):
                                color_url = 'https://www.nike.com' + color_url
                            color_variants.append({
                                'name': color_name,
                                'url': color_url
                            })
                    break
            
            product_info = {
                "Product Name": product_name or "N/A",
                "Price": final_price or "N/A",
                "Original Price": price if sale_price else "N/A",
                "Sale Price": sale_price or "N/A",
                "Stock": stock or "N/A",
                "Sizes Available": sizes_available,
                "Image URL": images[0] if images else None,
                "Additional Images": images[1:] if len(images) > 1 else [],
                "Description": description or "N/A",
                "Features": features or [],
                "Benefits": benefits or [],
                "Specifications": specifications or {},
                "Color Variants": color_variants or [],
                "Rating": "N/A",  # Nike doesn't show ratings on product pages
                "Reviews Count": "N/A"  # Nike doesn't show review counts on product pages
            }
            
            # Validate and load the main image
            if product_info["Image URL"]:
                try:
                    image_response = session.get(product_info["Image URL"], headers=headers)
                    img = Image.open(BytesIO(image_response.content))
                    product_info["Image"] = "Image loaded successfully"
                except Exception as e:
                    product_info["Image"] = f"Failed to load image: {e}"
            
            return product_info
            
        except requests.RequestException as e:
            retry_count += 1
            error_message = str(e)
            if retry_count == max_retries:
                print(f"Failed to fetch the webpage after {max_retries} attempts: {e}")
                return {
                    "error": f"Failed to access Nike. Error: {error_message}\n" +
                            "Please try:\n" +
                            "1. Check your internet connection\n" +
                            "2. Verify the URL is correct\n" +
                            "3. Try again in a few minutes"
                }
            continue
        except Exception as e:
            print(f"Unexpected error: {e}")
            return {
                "error": "An unexpected error occurred while scraping the product.\n" +
                        f"Error details: {str(e)}\n" +
                        "Please try again or contact support if the issue persists."
            }

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "URL is required"}), 400
    
    url = data['url']
    if not ('nike.com/in' in url or 'nike.in' in url):
        return jsonify({"error": "URL must be from nike.com/in"}), 400
    
    product_info = scrape_nike_product(url)
    if not product_info:
        return jsonify({"error": "Failed to scrape the product"}), 500
    
    if "error" in product_info:
        return jsonify(product_info), 400
    
    return jsonify(product_info)

if __name__ == '__main__':
    app.run(debug=True, port=5005) 