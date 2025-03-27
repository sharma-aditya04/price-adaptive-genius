# Problem Statement - 2
## AI-Powered Dynamic Pricing System

## Team Status200

## Description
### E-commerce platforms need to optimize pricing strategies tso remain competitive and maximize revenue. Traditional pricing models rely on static pricing, which fails to adapt to market fluctuations. A dynamic pricing system should analyse real-time demand, competitor pricing, and other factors to automatically adjust product prices, ensuring profitability and competitiveness.
## Key Requirements
- ## Real-Time Market Analysis
- Track competitor prices, stock availability, and demand trends.
- Use web scraping and APIs to gather live pricing data.
- ## AI/ML-Based Pricing Optimization
- Train models on historical sales data to identify optimal pricing strategies.
- Adjust prices dynamically based on demand, festive seasons, and customer behaviour.
- ## Custom Pricing Rules & Strategies
- Set predefined rules for discounts, seasonal pricing, and stock clearance.
- Implement surge pricing during high-demand periods.
- ## User & Competitor Insights
- Analyse customer behaviour to offer personalized price recommendations.
- Identify competitors’ pricing trends to adjust prices strategically.


## Project Video
[Watch our project demo video](https://drive.google.com/file/d/1pB8Hqqr7AFGWBhHRMgEX8jP37h-VYc72/view?usp=sharing)


# Price Adaptive Genius

A smart price tracking and comparison system that helps users find the best deals across multiple e-commerce platforms.

## Problem Solving Approach

1. **Data Collection**
   - Implemented robust web scrapers for multiple e-commerce platforms
   - Used rotating headers and anti-bot measures to avoid detection
   - Implemented rate limiting and error handling
   - Added support for different page layouts and selectors

2. **Data Processing**
   - Normalized data across different platforms
   - Implemented price cleaning and formatting
   - Added support for different currency formats
   - Created unified data structure for all products

3. **User Interface**
   - Designed responsive and modern UI
   - Implemented real-time price updates
   - Added product comparison features
   - Created intuitive navigation and search

4. **Performance Optimization**
   - Implemented caching for frequently accessed data
   - Used lazy loading for images
   - Optimized database queries
   - Added request rate limiting

## Tech Stack

### Frontend
- React.js
- TypeScript
- Material-UI
- Axios for API calls

### Backend
- Python 3.8+
- Flask
- BeautifulSoup4
- Requests
- Flask-CORS



### DevOps
- GitHub Actions

## Build and Run Commands

### Prerequisites
- Node.js (v14 or higher)
- Python 3.8 or higher

### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build
```

### Backend Setup
```bash
# Navigate to pybar directory
cd pybar

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start Flask server
python app.py
```

### Database Setup
```bash
# Create database
createdb price_adaptive_genius

# Run migrations
flask db upgrade
```

## API Endpoints

### Product Scraping
- `POST /api/scrape/amazon` - Scrape Amazon product details
- `POST /api/scrape/flipkart` - Scrape Flipkart product details
- `POST /api/scrape/myntra` - Scrape Myntra product details
- `POST /api/scrape/ajio` - Scrape AJIO product details

### Product Management
- `GET /api/products` - Get all products
- `GET /api/products/:id` - Get product details
- `POST /api/products` - Add new product
- `PUT /api/products/:id` - Update product
- `DELETE /api/products/:id` - Delete product

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


### Team Members

1. **Sumukh Bhende**
   - Contact: +91 7030421835
   - Email: sumukhsbhende@gmail.com
   - Role: Frontend Developer & Web Scraping Collector
   - Contribution: Developed the React frontend, implemented responsive design, created user interface components, and Scraped websites to collect live competitor market data.

2. **Aditya Sharma**
   - Contact: +91 8421057928
   - Email: adityaks@gmail.com
   - Role: Model Training & Database Specialist
   - Contribution: Built the Flask backend, implemented web scraping functionality, designed database schema, and handled API integrations.

3. **Sandhya Mourya**
   - Contact: +91 8459291370
   - Email: mouryasandhya25@gmail.com
   - Role: Dataset Collection , Preprocessing and Presentation
   - Contribution: Set up project infrastructure, collected dataset for model to train on and preparing for presentation

## Project Structure

```
price-adaptive-genius/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/      # Reusable React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   ├── styles/         # CSS and styling files
│   │   └── App.tsx         # Main application component
│   ├── public/             # Static assets
│   └── package.json        # Frontend dependencies
│
├── pybar/                   # Python backend services
│   ├── app.py              # Main Flask application
│   ├── amazon_scraper.py   # Amazon product scraper
│   ├── flipkart_scraper.py # Flipkart product scraper
│   ├── myntra_scraper.py   # Myntra product scraper
│   └── ajio_scraper.py     # AJIO product scraper
│
├── database/               # Database related files
│   └── schema.sql         # Database schema
│
└── README.md             # Project documentation
```
