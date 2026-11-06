import math

def parse_order(text):
    if not isinstance(text, str):
        raise TypeError("Order must be a string")

    if text.count(':') != 1:
        raise ValueError("Order must contain exactly one colon")

    garment, kg = text.split(':')

    garment = garment.strip()
    kg = kg.strip()

    if not garment:
        raise ValueError("Garment name cannot be empty")

    try:
        weight = float(kg)
    except ValueError:
        raise ValueError("Weight must be numeric")

    if not math.isfinite(weight) or weight < 0:
        raise ValueError("Weight must be finite and non-negative")

    return garment.title(), weight


def weight_average(weights_csv):
    if not isinstance(weights_csv, str):
        raise TypeError("Weights must be provided as a string")

    if not weights_csv.strip():
        raise ValueError("Weights cannot be empty")

    try:
        values = [int(r.strip()) for r in weights_csv.split(',')]
    except ValueError:
        raise ValueError("All weights must be integers")

    if any(value < 0 for value in values):
        raise ValueError("Weights cannot be negative")

    if not values:
        raise ValueError("At least one weight is required")

    return sum(values) // len(values)


def payable_charge(text):
    if not isinstance(text, str):
        raise TypeError("Charge details must be a string")

    if text.count('|') != 1:
        raise ValueError("Input must contain exactly one | separator")

    charge, discount = text.split('|')

    try:
        charge = float(charge.strip())
        discount = float(discount.strip())
    except ValueError:
        raise ValueError("Charge and discount must be numeric")

    if not math.isfinite(charge) or not math.isfinite(discount):
        raise ValueError("Charge and discount must be finite")

    if charge < 0 or discount < 0:
        raise ValueError("Charge and discount cannot be negative")

    total = charge * 1.18 - discount
    return max(total, 0)


def main():
    print("==== Running parse_order ====")
    user_input = input("Enter garment:weight in kg (e.g. regular:6): ")
    result = parse_order(user_input)
    print("Garment and Weight:", result)

    print("\n==== Running weight_average ====")
    user_input = input("Enter garment weights as CSV (e.g. 3,5,8): ")
    result = weight_average(user_input)
    print("Average Weight:", result)

    print("\n==== Running payable_charge ====")
    user_input = input("Enter charge|discount (e.g. 300|40): ")
    result = payable_charge(user_input)
    print("Payable Charge:", result)


if __name__ == "__main__":
    main()