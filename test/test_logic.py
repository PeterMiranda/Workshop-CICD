"""
Unit tests for Gym Logic validation and calculation.
"""
import pytest
from logic import calculate_total_cost, validate_selection

# Test Validation
def test_validation_success():
is_valid, msg = validate_selection("Basic", ["Personal Training"])
assert is_valid is True
assert msg == ""

def test_validation_invalid_plan():
is_valid, msg = validate_selection("NonExistentPlan", [])
assert is_valid is False
assert "Plan 'NonExistentPlan' does not exist" in msg

def test_validation_invalid_feature():
is_valid, msg = validate_selection("Basic", ["Space Travel"])
assert is_valid is False
assert "Feature 'Space Travel' is not available" in msg

# Test Calculation logic

def test_basic_calculation():
# Basic ($50) + Personal Training ($30) = 80.
# < 200, no discounts. 1 Member.
cost = calculate_total_cost("Basic", ["Personal Training"], 1)
assert cost == 80

def test_group_discount():
# Basic ($50) * 2 people = 100 base.
# Group discount 10% -> 100 - 10 = 90.
cost = calculate_total_cost("Basic", [], 2)
assert cost == 90

def test_premium_surcharge():
# Basic ($50) + Exclusive Access ($50) = 100.
# Exclusive Access is PREMIUM.
# Surcharge 15% of 100 = 15. Total 115.
cost = calculate_total_cost("Basic", ["Exclusive Access"], 1)
assert cost == 115

def test_special_offer_threshold_200():
# Family ($150) + Personal Training ($30) + Group Classes ($20) = 200 exactly.
# Let's push it over 200. Family ($150) + 2x Personal ($60 implied) -> let's use logic.
# Scenario: Family ($150) + Exclusive Access ($50) = 200.
# + Premium Surcharge (15% of 200 = 30) = 230.
# Total > 200, so -$20 discount.
# Final expected: 230 - 20 = 210.
cost = calculate_total_cost("Family", ["Exclusive Access"], 1)
assert cost == 210

def test_return_integer():
cost = calculate_total_cost("Basic", [], 1)
assert isinstance(cost, int)
