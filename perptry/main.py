# main.py (FastAPI)
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class PricingRequest(BaseModel):
    product_id: str
    user_segment: str
    market_data: dict

@app.post("/calculate-price")
async def calculate_price(request: PricingRequest):
    processor = DataProcessor()
    engine = PricingDecisionEngine()
    
    clean_data = processor.clean_data(request.market_data)
    features = processor.prepare_features(clean_data)
    
    optimal_price = engine.calculate_optimal_price(features)
    return {"product_id": request.product_id, "price": optimal_price}
