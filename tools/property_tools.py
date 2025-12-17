"""Property-related tools for real estate agents."""
import json
from typing import List, Dict, Optional
from datetime import datetime, timedelta


# Dummy property database - in production, this would be a real database
PROPERTIES_DB = [
    {
        "property_id": "PROP001",
        "title": "Modern 3BR Apartment in Downtown",
        "type": "apartment",
        "bedrooms": 3,
        "bathrooms": 2,
        "area_sqft": 1200,
        "price": 450000,
        "location": "Downtown",
        "address": "123 Main St, Downtown",
        "description": "Beautiful modern apartment with city views",
        "amenities": ["parking", "gym", "pool", "elevator"],
        "year_built": 2020,
        "available": True,
    },
    {
        "property_id": "PROP002",
        "title": "Luxury 4BR House with Garden",
        "type": "house",
        "bedrooms": 4,
        "bathrooms": 3,
        "area_sqft": 2500,
        "price": 850000,
        "location": "Suburbs",
        "address": "456 Oak Ave, Suburbs",
        "description": "Spacious family home with large garden",
        "amenities": ["garage", "garden", "fireplace"],
        "year_built": 2015,
        "available": True,
    },
    {
        "property_id": "PROP003",
        "title": "Cozy 2BR Condo Near Beach",
        "type": "condo",
        "bedrooms": 2,
        "bathrooms": 1,
        "area_sqft": 900,
        "price": 320000,
        "location": "Beachfront",
        "address": "789 Beach Blvd, Beachfront",
        "description": "Charming condo steps from the beach",
        "amenities": ["balcony", "parking"],
        "year_built": 2018,
        "available": True,
    },
    {
        "property_id": "PROP004",
        "title": "Penthouse 5BR with Rooftop",
        "type": "penthouse",
        "bedrooms": 5,
        "bathrooms": 4,
        "area_sqft": 4000,
        "price": 2500000,
        "location": "Downtown",
        "address": "321 Sky Tower, Downtown",
        "description": "Luxury penthouse with panoramic views",
        "amenities": ["rooftop", "concierge", "gym", "parking"],
        "year_built": 2022,
        "available": True,
    },
]


def search_properties(
    location: Optional[str] = None,
    property_type: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    bedrooms: Optional[int] = None,
    bathrooms: Optional[int] = None,
    min_area: Optional[float] = None,
    max_area: Optional[float] = None,
) -> str:
    """Search for properties based on criteria.
    
    Args:
        location: Location/city name
        property_type: Type of property (apartment, house, condo, penthouse)
        min_price: Minimum price
        max_price: Maximum price
        bedrooms: Number of bedrooms
        bathrooms: Number of bathrooms
        min_area: Minimum area in square feet
        max_area: Maximum area in square feet
    
    Returns:
        JSON string of matching properties
    """
    results = PROPERTIES_DB.copy()
    
    # Filter by criteria
    if location:
        results = [p for p in results if location.lower() in p["location"].lower()]
    
    if property_type:
        results = [p for p in results if p["type"].lower() == property_type.lower()]
    
    if min_price:
        results = [p for p in results if p["price"] >= min_price]
    
    if max_price:
        results = [p for p in results if p["price"] <= max_price]
    
    if bedrooms:
        results = [p for p in results if p["bedrooms"] >= bedrooms]
    
    if bathrooms:
        results = [p for p in results if p["bathrooms"] >= bathrooms]
    
    if min_area:
        results = [p for p in results if p["area_sqft"] >= min_area]
    
    if max_area:
        results = [p for p in results if p["area_sqft"] <= max_area]
    
    # Only return available properties
    results = [p for p in results if p["available"]]
    
    return json.dumps(results, indent=2)


def get_property_details(property_id: str) -> str:
    """Get detailed information about a specific property.
    
    Args:
        property_id: The property ID
    
    Returns:
        JSON string with property details
    """
    property_data = next(
        (p for p in PROPERTIES_DB if p["property_id"] == property_id),
        None
    )
    
    if not property_data:
        return json.dumps({"error": f"Property {property_id} not found"})
    
    return json.dumps(property_data, indent=2)


def estimate_property_value(
    property_type: str,
    bedrooms: int,
    bathrooms: int,
    area_sqft: float,
    location: str,
    year_built: Optional[int] = None,
) -> str:
    """Estimate the market value of a property based on features.
    
    Args:
        property_type: Type of property
        bedrooms: Number of bedrooms
        bathrooms: Number of bathrooms
        area_sqft: Area in square feet
        location: Location/city
        year_built: Year the property was built
    
    Returns:
        JSON string with estimated value and breakdown
    """
    # Simple estimation algorithm (in production, use ML model or market data)
    base_price_per_sqft = {
        "apartment": 350,
        "house": 400,
        "condo": 300,
        "penthouse": 600,
    }
    
    base_price = base_price_per_sqft.get(property_type.lower(), 350) * area_sqft
    
    # Adjustments
    bedroom_multiplier = 1 + (bedrooms - 2) * 0.1
    bathroom_multiplier = 1 + (bathrooms - 1) * 0.05
    
    # Location premium (dummy values)
    location_multipliers = {
        "downtown": 1.3,
        "suburbs": 1.0,
        "beachfront": 1.5,
    }
    location_mult = location_multipliers.get(location.lower(), 1.0)
    
    # Age depreciation
    if year_built:
        age = datetime.now().year - year_built
        age_multiplier = max(0.7, 1 - (age * 0.01))
    else:
        age_multiplier = 1.0
    
    estimated_value = base_price * bedroom_multiplier * bathroom_multiplier * location_mult * age_multiplier
    
    return json.dumps({
        "estimated_value": round(estimated_value, 2),
        "price_per_sqft": round(estimated_value / area_sqft, 2),
        "breakdown": {
            "base_price": round(base_price, 2),
            "bedroom_adjustment": f"{bedroom_multiplier:.2f}x",
            "bathroom_adjustment": f"{bathroom_multiplier:.2f}x",
            "location_adjustment": f"{location_mult:.2f}x",
            "age_adjustment": f"{age_multiplier:.2f}x",
        }
    }, indent=2)


def get_similar_properties(property_id: str, limit: int = 3) -> str:
    """Find similar properties to a given property.
    
    Args:
        property_id: The property ID to find similar properties for
        limit: Maximum number of similar properties to return
    
    Returns:
        JSON string with similar properties
    """
    property_data = next(
        (p for p in PROPERTIES_DB if p["property_id"] == property_id),
        None
    )
    
    if not property_data:
        return json.dumps({"error": f"Property {property_id} not found"})
    
    # Find similar properties based on type, location, and price range
    similar = []
    for prop in PROPERTIES_DB:
        if prop["property_id"] == property_id:
            continue
        
        similarity_score = 0
        
        if prop["type"] == property_data["type"]:
            similarity_score += 3
        
        if prop["location"] == property_data["location"]:
            similarity_score += 2
        
        price_diff = abs(prop["price"] - property_data["price"]) / property_data["price"]
        if price_diff < 0.2:  # Within 20% price range
            similarity_score += 2
        
        if prop["bedrooms"] == property_data["bedrooms"]:
            similarity_score += 1
        
        if similarity_score >= 3:
            prop_copy = prop.copy()
            prop_copy["similarity_score"] = similarity_score
            similar.append(prop_copy)
    
    # Sort by similarity score and limit
    similar.sort(key=lambda x: x["similarity_score"], reverse=True)
    similar = similar[:limit]
    
    return json.dumps(similar, indent=2)

