"""Market analysis and financial tools for real estate."""
import json
from typing import Optional


def calculate_mortgage(
    property_price: float,
    down_payment: float,
    interest_rate: float,
    loan_term_years: int = 30,
) -> str:
    """Calculate monthly mortgage payment.
    
    Args:
        property_price: Total property price
        down_payment: Down payment amount
        interest_rate: Annual interest rate (as decimal, e.g., 0.05 for 5%)
        loan_term_years: Loan term in years (default 30)
    
    Returns:
        JSON string with mortgage calculation details
    """
    loan_amount = property_price - down_payment
    
    if loan_amount <= 0:
        return json.dumps({"error": "Down payment must be less than property price"})
    
    monthly_rate = interest_rate / 12
    num_payments = loan_term_years * 12
    
    # Mortgage formula: M = P * [r(1+r)^n] / [(1+r)^n - 1]
    if monthly_rate == 0:
        monthly_payment = loan_amount / num_payments
    else:
        monthly_payment = loan_amount * (
            (monthly_rate * (1 + monthly_rate) ** num_payments) /
            ((1 + monthly_rate) ** num_payments - 1)
        )
    
    total_paid = monthly_payment * num_payments
    total_interest = total_paid - loan_amount
    
    return json.dumps({
        "property_price": property_price,
        "down_payment": down_payment,
        "loan_amount": round(loan_amount, 2),
        "interest_rate": f"{interest_rate * 100:.2f}%",
        "loan_term_years": loan_term_years,
        "monthly_payment": round(monthly_payment, 2),
        "total_paid": round(total_paid, 2),
        "total_interest": round(total_interest, 2),
        "down_payment_percentage": round((down_payment / property_price) * 100, 2)
    }, indent=2)


def get_market_trends(location: str) -> str:
    """Get market trends for a location.
    
    Args:
        location: Location/city name
    
    Returns:
        JSON string with market trends
    """
    # Dummy market data - in production, fetch from real estate APIs
    trends = {
        "downtown": {
            "average_price": 450000,
            "price_change_3mo": "+5.2%",
            "price_change_1yr": "+12.5%",
            "days_on_market_avg": 45,
            "inventory_level": "low",
            "market_sentiment": "seller's market",
            "price_per_sqft": 375,
        },
        "suburbs": {
            "average_price": 650000,
            "price_change_3mo": "+3.8%",
            "price_change_1yr": "+8.9%",
            "days_on_market_avg": 60,
            "inventory_level": "moderate",
            "market_sentiment": "balanced",
            "price_per_sqft": 260,
        },
        "beachfront": {
            "average_price": 850000,
            "price_change_3mo": "+7.1%",
            "price_change_1yr": "+15.3%",
            "days_on_market_avg": 30,
            "inventory_level": "very low",
            "market_sentiment": "strong seller's market",
            "price_per_sqft": 550,
        },
    }
    
    location_key = location.lower()
    trend_data = trends.get(location_key, {
        "average_price": 500000,
        "price_change_3mo": "+4.0%",
        "price_change_1yr": "+10.0%",
        "days_on_market_avg": 50,
        "inventory_level": "moderate",
        "market_sentiment": "balanced",
        "price_per_sqft": 300,
    })
    
    trend_data["location"] = location
    return json.dumps(trend_data, indent=2)


def compare_properties(property_ids: list[str]) -> str:
    """Compare multiple properties side by side.
    
    Args:
        property_ids: List of property IDs to compare
    
    Returns:
        JSON string with property comparison
    """
    from tools.property_tools import PROPERTIES_DB
    
    properties = [
        prop for prop in PROPERTIES_DB
        if prop["property_id"] in property_ids
    ]
    
    if not properties:
        return json.dumps({"error": "No properties found"})
    
    comparison = {
        "properties": properties,
        "summary": {
            "count": len(properties),
            "price_range": {
                "min": min(p["price"] for p in properties),
                "max": max(p["price"] for p in properties),
                "avg": sum(p["price"] for p in properties) / len(properties),
            },
            "bedroom_range": {
                "min": min(p["bedrooms"] for p in properties),
                "max": max(p["bedrooms"] for p in properties),
            },
            "area_range": {
                "min": min(p["area_sqft"] for p in properties),
                "max": max(p["area_sqft"] for p in properties),
                "avg": sum(p["area_sqft"] for p in properties) / len(properties),
            },
        }
    }
    
    return json.dumps(comparison, indent=2)

