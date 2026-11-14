
"""Predefined Python bug examples for the Gradio UI."""

EXAMPLES = {
    "Division by Zero": {
        "code": (
            "def divide_two_numbers(a, b):\n"
            "    return a / b"
        ),
        "args": "[10, 0]",
    },

    "Invalid Coupon Code": {
        "code": (
            "def apply_coupon_code(cart_total, coupon_code):\n"
            "    coupons = {'SAVE10': 0.10, 'SAVE20': 0.20}\n"
            "    discount = coupons[coupon_code]\n"
            "    return cart_total * (1 - discount)"
        ),
        "args": '[100, "INVALID"]',
    },

    "Product Index Out of Range": {
        "code": (
            "def get_product_price(products, product_id):\n"
            "    return products[product_id]['price']"
        ),
        "args": '[[{"price": 10}, {"price": 20}], 5]',
    },

    "Format Price - None Value": {
        "code": (
            'def format_price_display(price):\n'
            '    return f"${price:.2f}"'
        ),
        "args": "[null]",
    },

    "Bulk Discount - Zero Quantity": {
        "code": (
            "def calculate_bulk_discount(quantity, unit_price):\n"
            "    avg_discount = 100 / quantity\n"
            "    if quantity >= 100:\n"
            "        discount = 0.20\n"
            "    elif quantity >= 50:\n"
            "        discount = 0.10\n"
            "    else:\n"
            "        discount = 0.0\n"
            "    return quantity * unit_price * (1 - discount)"
        ),
        "args": "[0, 10.99]",
    },
}