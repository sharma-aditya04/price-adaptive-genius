# test_pricing.py (pytest)
import pytest

def test_price_calculation():
    engine = PricingDecisionEngine()
    test_case = {
        'demand': 0.85,
        'competitor_price': 100,
        'min_cost': 80
    }
    price = engine.calculate_optimal_price(test_case)
    assert 80 <= price <= 110
