# pricing_engine.py
import numpy as np

class PricingDecisionEngine:
    def __init__(self, model, min_margin=0.2):
        self.model = model
        self.min_margin = min_margin
    
    def calculate_optimal_price(self, features):
        base_price = self.model.predict(features)
        competitor_price = features['competitor_price']
        
        # Strategic pricing rules
        if features['demand'] > 0.8:
            price = min(base_price * 1.15, competitor_price * 0.98)
        elif features['demand'] < 0.3:
            price = max(base_price * 0.9, self.min_cost * (1 + self.min_margin))
        else:
            price = base_price
            
        return np.clip(price, self.min_cost, competitor_price * 1.1)
