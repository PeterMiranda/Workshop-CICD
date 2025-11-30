"""
Business logic for Gym Membership calculations.
"""
from src.config import (
    MEMBERSHIP_PLANS,
    ADDITIONAL_FEATURES,
    GROUP_DISCOUNT_THRESHOLD,
    GROUP_DISCOUNT_RATE,
    PREMIUM_SURCHARGE_RATE,
    SPECIAL_OFFERS
)

def validate_selection(plan_name, features):
    """
    Validates if the plan and features exist in configuration.
    Returns (True, "") or (False, error_message).
    """
    if plan_name not in MEMBERSHIP_PLANS:
        return False, f"Error: Plan '{plan_name}' does not exist."
    for feature in features:
        if feature not in ADDITIONAL_FEATURES:
            return False, f"Error: Feature '{feature}' is not available."
    return True, ""

def calculate_total_cost(plan_name, features, member_count):
    """
    Calculates the final cost based on requirements.
    
    Args:
        plan_name (str): The selected membership plan.
        features (list): List of strings of selected features.
        member_count (int): Number of people signing up.

    Returns:
        int: The final calculated cost.
    """
    # 1. Base Cost
    base_cost = MEMBERSHIP_PLANS[plan_name]["base_cost"]
    # 2. Features Cost
    features_cost = sum(ADDITIONAL_FEATURES[f]["cost"] for f in features)
    # Subtotal per person (This assumption implies features are per membership group)
    # Adjust logic here if features are charged per person individually.
    # Assumption: The base plan covers the group if it's "Family",
    # but strictly following the prompt: "If two or more members sign up... apply discount"
    # Usually implies: (Base + Features) * Members * Discount.
    # Let's assume the cost calculated is for the entire billing group.
    raw_total = base_cost + features_cost
    if plan_name != "Family":
        # If it's not a family plan, we assume cost is per person
        raw_total = raw_total * member_count
    # 3. Discounts for Group Memberships (Req 2)
    current_total = raw_total
    if member_count >= GROUP_DISCOUNT_THRESHOLD:
        current_total -= (current_total * GROUP_DISCOUNT_RATE)
    # 4. Premium Membership Features Surcharge (Req 4)
    # Check if any selected feature is premium
    has_premium_feature = any(ADDITIONAL_FEATURES[f]["is_premium"] for f in features)

    if has_premium_feature:
        current_total += (current_total * PREMIUM_SURCHARGE_RATE)
    # 5. Special Offer Discounts (Req 3)
    # Check thresholds (Order matters: Check highest first usually, or cumulative?)
    # Req says: "If cost exceeds 200 apply 20", "If exceeds 400 apply 50".
    # Typically these are non-cumulative brackets.
    discount_amount = 0
    for offer in SPECIAL_OFFERS:
        if current_total > offer["threshold"]:
            discount_amount = offer["discount"]
            break # Apply only the highest applicable discount
    current_total -= discount_amount
    # Ensure output is integer and positive
    return int(current_total)
