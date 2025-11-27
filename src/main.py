"""
Main entry point for the Gym Management System CLI.
"""

from config import MEMBERSHIP_PLANS, ADDITIONAL_FEATURES
from logic import calculate_total_cost, validate_selection


def display_menu():
    print("\n--- GYM MEMBERSHIP SYSTEM ---")
    print("Available Plans:")
    for plan, details in MEMBERSHIP_PLANS.items():
        print(f" - {plan}: ${details['base_cost']} ({details['description']})")

    print("\nAvailable Features:")
    for feature, details in ADDITIONAL_FEATURES.items():
        premium_tag = " [PREMIUM]" if details["is_premium"] else ""
        print(f" - {feature}: ${details['cost']}{premium_tag}")


def get_user_input():
    try:
        plan = input("\nSelect Membership Plan: ").strip()
        print("Enter additional features separated by comma (or press enter for none):")
        features_input = input("> ").strip()
        features = (
            [f.strip() for f in features_input.split(",")] if features_input else []
        )
        members = int(input("How many members are signing up? "))
        if members < 1:
            raise ValueError("Member count must be at least 1.")
        return plan, features, members
    except ValueError as e:
        print(f"Input Error: {e}")
        return None, None, None


def run_app():
    display_menu()
    plan, features, members = get_user_input()
    if not plan:
        return -1
    # Validation (Req 5 & 8)
    is_valid, message = validate_selection(plan, features)
    if not is_valid:
        print(message)
        return -1
    # Calculate preliminary cost for confirmation
    try:
        final_cost = calculate_total_cost(plan, features, members)
        # User Confirmation (Req 6)
        print("\n--- CONFIRMATION ---")
        print(f"Plan: {plan}")
        print(f"Features: {', '.join(features) if features else 'None'}")
        print(f"Members: {members}")
        print(f"Calculated Total Cost: ${final_cost}")
        confirm = input("Confirm subscription? (yes/no): ").lower()
        if confirm == "yes":
            print(f"Success! Total to pay: ${final_cost}")
            return final_cost
        else:
            print("Cancelled by user.")
            return -1
    except Exception as e:
        print(f"Calculation Error: {e}")
        return -1


if __name__ == "__main__":
    result = run_app()
    # Requirement 7: Output return logic
    if __name__ == "__main__":
        import sys

        sys.exit(0 if result != -1 else 1)
