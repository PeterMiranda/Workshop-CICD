"""
Main entry point for the Gym Management System CLI.
Provides user interaction for selecting membership plans,
optional additional features, and calculating subscription costs.
"""

from src.config import MEMBERSHIP_PLANS, ADDITIONAL_FEATURES
from src.logic import calculate_total_cost, validate_selection


def display_menu():
    """
    Display all available gym membership plans and optional features.
    """
    print("\n--- GYM MEMBERSHIP SYSTEM ---")
    print("Available Plans:")
    for plan, details in MEMBERSHIP_PLANS.items():
        print(f" - {plan}: ${details['base_cost']} ({details['description']})")

    print("\nAvailable Features:")
    for feature, details in ADDITIONAL_FEATURES.items():
        premium_tag = " [PREMIUM]" if details["is_premium"] else ""
        print(f" - {feature}: ${details['cost']}{premium_tag}")


def get_user_input():
    """
    Request membership selections from the user.

    Returns:
        tuple: (plan_name (str), features (list[str]), members (int))
        Returns (None, None, None) if input fails validation.
    """
    try:
        plan = input("\nSelect Membership Plan: ").strip()

        print("Enter additional features separated by comma (or press enter for none):")
        features_raw = input("> ").strip()
        features = [f.strip() for f in features_raw.split(",")] if features_raw else []

        members = int(input("How many members are signing up? "))

        if members < 1:
            raise ValueError("Member count must be at least 1.")

        return plan, features, members

    except (ValueError, TypeError) as e:
        print(f"Input Error: {e}")

    return None, None, None


def run_app():
    """
    Main application flow:
        - Display menu
        - Collect user input
        - Validate selections
        - Calculate cost
        - Request confirmation

    Returns:
        int: Final total cost, or -1 if the process fails or is cancelled.
    """
    display_menu()

    plan, features, members = get_user_input()
    if plan is None:
        return -1

    # Validate selection
    is_valid, message = validate_selection(plan, features)
    if not is_valid:
        print(message)
        return -1

    # Calculate cost
    total_cost = calculate_total_cost(plan, features, members)

    # Confirm with user
    print("\n--- CONFIRMATION ---")
    print(f"Plan: {plan}")
    print(f"Features: {', '.join(features) if features else 'None'}")
    print(f"Members: {members}")
    print(f"Calculated Total Cost: ${total_cost}")

    confirm = input("Confirm subscription? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Cancelled by user.")
        return -1

    print(f"Success! Total to pay: ${total_cost}")
    return total_cost


if __name__ == "__main__":
    RESULT = run_app()

    # Requirement 7: return specific exit codes
    import sys

    sys.exit(0 if RESULT != -1 else 1)
