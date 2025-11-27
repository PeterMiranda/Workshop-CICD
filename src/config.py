"""
Configuration file for Gym Membership System.
Contains pricing, available plans, and features.
"""

MEMBERSHIP_PLANS = {
    "Basic": {"base_cost": 50, "description": "Access to gym equipment"},
    "Premium": {"base_cost": 100, "description": "Gym + Sauna + Pool"},
    "Family": {"base_cost": 150, "description": "Access for 4 family members"}
}

ADDITIONAL_FEATURES = {
    "Personal Training": {"cost": 30, "is_premium": False},
    "Group Classes": {"cost": 20, "is_premium": False},
    "Exclusive Access": {"cost": 50, "is_premium": True},  # Triggers 15% surcharge
    "Diet Plan": {"cost": 10, "is_premium": False}
}

# Assumptions:
# 1. Group discount applies to the subtotal before fixed amount discounts.
# 2. Premium surcharge applies if ANY selected feature is premium.
GROUP_DISCOUNT_THRESHOLD = 2
GROUP_DISCOUNT_RATE = 0.10  # 10%
PREMIUM_SURCHARGE_RATE = 0.15 # 15%

SPECIAL_OFFERS = [
    {"threshold": 400, "discount": 50},
    {"threshold": 200, "discount": 20}
]
