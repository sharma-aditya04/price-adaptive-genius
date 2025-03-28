from bs4 import BeautifulSoup
import requests
import re
import random
from difflib import get_close_matches

def clean_price(price_text):
    if not price_text:
        return None
    return re.sub(r'[^\d.]', '', price_text)

def get_random_headers():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Firefox/122.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15",
    ]
    return {
        "User-Agent": random.choice(user_agents),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    }

def scrape_amazon_product(url):
    if 'amazon.in' not in url:
        print("Error: URL must be from amazon.in")
        return

    try:
        headers = get_random_headers()
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract brand
        brand = soup.find('a', {'id': 'bylineInfo'})
        brand = brand.text.strip().replace('Visit the ', '').replace(' Store', '') if brand else None

        # Extract prices
        original_price_element = soup.find("span", class_="a-size-small aok-offscreen")
        original_price = clean_price(original_price_element.text).lstrip('.') if original_price_element else None

        listed_price_element = soup.find("span", class_="a-price-whole")
        listed_price_fraction = soup.find("span", class_="a-price-fraction")
        listed_price = clean_price(listed_price_element.text) if listed_price_element else None
        if listed_price and listed_price_fraction:
            listed_price += listed_price_fraction.text.strip()

        # Determine sale flag using the clearance/sale badge
        sale_flag_element = soup.find("span", class_="a-size-small dealBadgeTextColor a-text-bold")
        sale_flag = bool(sale_flag_element)

        ## product name
        product_name_element = soup.find("span", class_="a-size-large product-title-word-break")
        product_name = product_name_element.text.strip() if product_name_element else None

        # Print the results
        print("Brand:", brand)
        print("Product Name:", product_name)
        print("Original Price:", original_price)
        print("Listed Price:", listed_price)
        print("Clearance/Sale Flag:", sale_flag)
        return product_name  # Return the product name for further processing
    except Exception as e:
        print("Error:", str(e))

# Example usage
url = input("Enter the Amazon.in product URL: ")
product_name=scrape_amazon_product(url)

def search_flipkart(product_name):
    try:
        # Clean and shorten the product name for better search results
        # Clean and shorten the product name for better search results
        search_query = "+".join(re.sub(r'[^\w\s]', '', product_name).split()[:5])  # Remove special characters and use the first 5 words
        flipkart_search_url = f"https://www.flipkart.com/search?q={search_query}"

        # Helper function to find the closest matching product name
        def find_closest_match(product_name, product_list):
            return get_close_matches(product_name, product_list, n=1, cutoff=0.6)  # Adjust cutoff for similarity threshold

        headers = get_random_headers()
        response = requests.get(flipkart_search_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the first product's price
        price_element = soup.find("div", class_="Nx9bqj CxhGGd")
        flipkart_price = clean_price(price_element.text) if price_element else None

        # Extract the first product's name
        product_name_element = soup.find("a", class_="IRpwTa") or soup.find("a", class_="_1fQZEK")
        flipkart_product_name = product_name_element.text.strip() if product_name_element else None

        # Print the results
        if flipkart_price and flipkart_product_name:
            print("Flipkart Product Name:", flipkart_product_name)
            print("Flipkart Price:", flipkart_price)
        else:
            flipkart_url = input("Enter the Flipkart product URL (or enter 0 if the product is not on Flipkart): ")
            if flipkart_url == "0":
                print("Product is not available on Flipkart.")
            else:
                try:
                    headers = get_random_headers()
                    response = requests.get(flipkart_url, headers=headers)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Extract price from the provided Flipkart URL
                    price_element = soup.find("div", class_="Nx9bqj CxhGGd")
                    flipkart_price = clean_price(price_element.text) if price_element else None

                    # Extract product name from the provided Flipkart URL
                    product_name_element = soup.find("span", class_="VU-ZEz")
                    flipkart_product_name = product_name_element.text.strip() if product_name_element else None

                    print("Flipkart Product Name:", flipkart_product_name)
                    print("Flipkart Price:", flipkart_price)
                except Exception as e:
                    print("Error while scraping Flipkart URL:", str(e))

    except Exception as e:
        print("Error while searching Flipkart:", str(e))


# Example usage
if product_name:
    search_flipkart(product_name)


