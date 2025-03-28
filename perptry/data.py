# Web Scraper (BeautifulSoup + Requests)
import requests
from bs4 import BeautifulSoup
import json

class CompetitorScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        }
    
    def scrape_amazon(self, product_url):
        response = requests.get(product_url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        return {
            'price': float(soup.select_one('span.a-price-whole').text.replace(',', '')),
            'stock': 'In stock' in soup.text,
            'rating': float(soup.select_one('span.a-icon-alt').text.split()[0])
        }

# API Client (Example: PriceAPI)
import httpx

class PriceAPIClient:
    def __init__(self, api_key):
        self.base_url = "https://api.priceapi.com/v2"
        self.session = httpx.AsyncClient(headers={"Authorization": f"Bearer {api_key}"})
    
    async def get_market_data(self, product_id):
        response = await self.session.get(
            f"{self.base_url}/products/{product_id}/offers"
        )
        return response.json()
