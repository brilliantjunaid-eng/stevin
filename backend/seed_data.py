"""Seed data for PJ Ours — menu items with size variants per PDF, outlets, popular items."""

# Items with 3-size pricing (S/M/L) per the original menu PDF
# Tuple format: (name, small, medium, large, popular?)
JUICE = [
    ("Anar", 60, 120, 230, False),
    ("Apple", 50, 105, 200, False),
    ("Carrot", 40, 85, 160, False),
    ("Cucumber", 40, 85, 160, False),
    ("Cucumber Lemon", 40, 85, 160, False),
    ("Gooseberry & Kanthari", 60, 125, 240, False),
    ("Grape", 40, 85, 160, False),
    ("Guava Lemon", 40, 85, 160, False),
    ("Kiwi", 80, 165, 320, False),
    ("Lemon (Fresh)", 30, 65, 120, False),
    ("Lemon Soda (Chilli)", 30, 65, 120, False),
    ("Lemon Grape", 40, 85, 160, False),
    ("Lemon Mint", 40, 85, 160, False),
    ("Lemon Pineapple", 40, 85, 160, False),
    ("Mango", 60, 125, 240, False),
    ("Mosambi", 50, 105, 200, False),
    ("Muskmelon (Shamam)", 40, 85, 160, False),
    ("Orange", 50, 105, 200, False),
    ("Orange Lemon", 50, 105, 200, False),
    ("Papaya", 40, 85, 160, False),
    ("Passion Fruit", 70, 145, 280, False),
    ("Pineapple", 50, 105, 200, False),
    ("Strawberry", 60, 125, 240, False),
    ("Water Melon", 40, 85, 160, False),
]

FUSION_SHAKE = [
    ("Apple Chickoo", 60, 125, 245, False),
    ("Apple Papaya", 60, 125, 245, False),
    ("Badam Pista", 60, 125, 245, False),
]

AVIL_MILK = [
    ("Chickoo Chocolate", 60, 125, 245, False),
    ("Chickoo Sharjah", 60, 125, 245, False),
    ("Chickoo Custard Apple", 60, 125, 245, False),
    ("Chocolate Caramel", 60, 125, 245, False),
    ("Chocolate Oreo", 60, 125, 245, False),
    ("Chocolate Sharjah", 60, 125, 245, False),
    ("Grape Pineapple", 60, 125, 245, False),
    ("Kitkat Oreo", 60, 125, 245, False),
    ("Oreo Caramel", 60, 125, 245, False),
    ("Oreo Sharjah", 60, 125, 245, False),
    ("Papaya Chickoo", 60, 125, 245, False),
    ("Papaya Mango", 60, 125, 245, False),
    ("Papaya Sharjah", 60, 125, 245, False),
    ("Saudi Caramel", 60, 125, 245, False),
    ("Sharjah Saudi", 60, 125, 245, False),
    ("Tender Butter", 80, 165, 325, False),
    ("Tender Cashew", 80, 165, 325, False),
    ("Tender Chickoo", 80, 165, 325, False),
    ("Tender Dates", 80, 165, 325, False),
    ("Tender Mango", 80, 165, 325, False),
    ("Tender Caramel", 80, 165, 325, False),
    ("Tender Chocolate", 80, 165, 325, True),  # popular
]

MILK_SHAKE = [
    ("Apple", 50, 105, 200, False),
    ("Avocado (Butter)", 60, 125, 240, True),  # popular
    ("Avocado Honey", 90, 185, 360, False),
    ("Badam", 40, 85, 160, False),
    ("Banana", 40, 85, 160, False),
    ("Blueberry", 60, 125, 240, False),
    ("Boost", 60, 125, 240, False),
    ("Brownie", 60, 125, 240, False),
    ("Butterscotch", 50, 105, 200, False),
]

DESSERTS = [
    ("Caramel", 50, 105, 200, False),
    ("Cherry (Kashmiri)", 40, 85, 160, False),
    ("Chickoo", 50, 105, 200, False),
    ("Chocolate", 40, 85, 160, False),
    ("Coffee Blast", 60, 125, 240, False),
    ("Cold Coffee", 50, 105, 200, False),
    ("Custard Apple", 50, 105, 200, False),
    ("Dark Fantasy", 45, 95, 180, False),
    ("Dates (Saudi)", 40, 85, 160, False),
    ("Dry Fruits", 60, 125, 240, False),
    ("Grape", 40, 85, 160, False),
    ("Guava", 40, 85, 160, False),
    ("Horlicks", 50, 105, 200, False),
    ("Ice Apple (Pananongu)", 50, 105, 200, False),
    ("Jack Fruit", 55, 115, 220, False),
    ("Malai Kulfi", 80, 165, 320, False),
    ("Kiwi", 80, 165, 320, False),
    ("Lotus Biscoff", 85, 175, 340, False),
    ("Mango", 60, 125, 240, False),
    ("Mixed Fruit", 50, 105, 200, False),
    ("Muskmelon (Shamam)", 40, 85, 160, False),
    ("Oreo", 40, 85, 160, True),  # popular
    ("Papaya", 40, 85, 160, False),
    ("Peanut Butter", 80, 165, 320, False),
    ("Pineapple", 40, 85, 160, False),
    ("Pista", 40, 85, 160, False),
    ("Pomegranate", 60, 125, 240, False),
    ("Strawberry", 50, 105, 200, False),
    ("Special Dry Fruits", 90, 185, 360, False),
    ("Vanilla", 40, 85, 160, False),
    ("Tender Coconut", 70, 145, 280, False),
]

MOCKTAIL = [
    ("Carrot Pineapple", 60, 125, 245, False),
    ("Grape Pineapple", 60, 125, 245, False),
    ("Mosambi Orange", 60, 125, 245, False),
    ("Papaya Pineapple", 60, 125, 245, False),
    ("Papaya Carrot", 60, 125, 245, False),
    ("Shamam Mango", 60, 125, 245, False),
    ("Shamam Papaya", 60, 125, 245, False),
    ("Water Melon Carrot", 60, 125, 245, False),
]

# Single-price categories (as per PDF)
ICE_CREAM_SHAKES = [
    ("Black Currant", 90, False), ("Butterscotch", 90, False),
    ("Choco Chips", 90, False), ("Chocolate", 90, False),
    ("English Delight", 90, False), ("Fig Dates And Honey", 90, False),
    ("Mango", 90, False), ("Mocha", 90, False),
    ("Pineapple", 90, False), ("Pista", 90, False),
    ("Red Velvet", 90, False), ("Strawberry", 90, False),
    ("Vancho", 90, False), ("Vanilla", 90, False),
    ("Banana Mastani", 90, False), ("Mango Mastani", 90, False),
    ("Papaya Mastani", 90, False), ("Pineapple Mastani", 90, True),  # popular
    ("Avocado Galaxy", 100, False), ("Banana Galaxy", 100, False),
    ("Caramel Galaxy", 100, False), ("Chickoo Galaxy", 100, False),
    ("Grape Galaxy", 100, False), ("Mango Galaxy", 100, False),
    ("Oreo Galaxy", 100, False), ("Papaya Galaxy", 100, False),
    ("Pineapple Galaxy", 100, False), ("Saudi Galaxy", 100, False),
    ("Tender Galaxy", 100, False),
]

FALOODA = [
    ("Cake Falooda", 150, False), ("Chocolate Falooda", 140, False),
    ("Dry Fruits Falooda", 150, False), ("Gulab Jam Falooda", 150, False),
    ("Mango Falooda", 140, False), ("Royal Falooda", 150, True),  # popular
    ("Strawberry Falooda", 140, False), ("Pineapple Falooda", 140, False),
    ("Fruit Punch Falooda", 160, False), ("Kulfi Falooda", 160, False),
]

ICE_CREAM = [
    ("Chocolate Brownie Magic", 120, False),
    ("Caramel Mocha Sundae", 120, False),
    ("Double Chocolate Cookie Fiesta", 120, False),
    ("Dry Fruits with Cake", 120, False),
    ("Wafer Crown with Cookie", 120, False),
    ("Dark Vanila With Coffee Fills", 120, False),
    ("Fruit Salad", 70, False),
    ("Sizzling Brownie Vanila", 120, False),
    ("Chocolate Sizzler", 160, False),
    ("Strawberry Sizzler", 160, False),
    ("Single Scoop", 30, False),
    ("Double Scoop", 50, False),
]

FRUIT_SODA = [
    ("Anar Soda", 40, False), ("Apple Soda", 40, False),
    ("Carrot Soda", 40, False), ("Grape Soda", 40, False),
    ("Guava Soda", 40, False), ("Mango Soda", 40, False),
    ("Mosambi Soda", 40, False), ("Orange Soda", 40, False),
    ("Passion Fruit Soda", 50, False), ("Pineapple Soda", 40, False),
    ("Shamam Soda", 40, False),
]

MOJITO = [
    ("Blue Curacao", 80, False), ("Blueberry", 80, False),
    ("Green Apple", 80, False), ("Green Seed", 80, False),
    ("Hot Gooseberry (spicy)", 80, False), ("Kiwi", 80, False),
    ("Litchi", 80, False), ("Mango Slice", 80, False),
    ("Mexican", 80, False), ("Mint", 80, True),  # popular
    ("Red Flame", 80, False), ("Red Freeze", 80, False),
    ("Valencia (Orange)", 80, False), ("Virgin", 50, False),
    ("Wineyard (Grape)", 80, False), ("Yellow Flower (Pineapple)", 80, False),
]

# Categories in display order
CATEGORIES_ORDER = [
    "Juice", "Fusion Shake", "Avil Milk", "Milk Shake", "Desserts",
    "Ice Cream Shakes", "Falooda", "Ice Cream", "Fruit Soda", "Mocktail", "Mojito",
]

SIZED_CATEGORIES = {
    "Juice": JUICE,
    "Fusion Shake": FUSION_SHAKE,
    "Avil Milk": AVIL_MILK,
    "Milk Shake": MILK_SHAKE,
    "Desserts": DESSERTS,
    "Mocktail": MOCKTAIL,
}

SINGLE_PRICE_CATEGORIES = {
    "Ice Cream Shakes": ICE_CREAM_SHAKES,
    "Falooda": FALOODA,
    "Ice Cream": ICE_CREAM,
    "Fruit Soda": FRUIT_SODA,
    "Mojito": MOJITO,
}


def build_menu_seed():
    """Return a list of menu item dicts ready to insert into MongoDB."""
    items = []
    position = 0
    popular_position = 0

    for cat in CATEGORIES_ORDER:
        if cat in SIZED_CATEGORIES:
            for (name, s, m, l, popular) in SIZED_CATEGORIES[cat]:
                items.append({
                    "category": cat,
                    "name": name,
                    "base_price": s,
                    "sizes": [
                        {"label": "Small", "price": s},
                        {"label": "Medium", "price": m},
                        {"label": "Large", "price": l},
                    ],
                    "image_url": None,
                    "active": True,
                    "popular": popular,
                    "popular_order": (popular_position := popular_position + 1) if popular else 0,
                    "position": (position := position + 1),
                })
        elif cat in SINGLE_PRICE_CATEGORIES:
            for (name, price, popular) in SINGLE_PRICE_CATEGORIES[cat]:
                items.append({
                    "category": cat,
                    "name": name,
                    "base_price": price,
                    "sizes": [],  # single price, no variants
                    "image_url": None,
                    "active": True,
                    "popular": popular,
                    "popular_order": (popular_position := popular_position + 1) if popular else 0,
                    "position": (position := position + 1),
                })
    return items


OUTLETS_SEED = [
    {
        "id": "eastfort",
        "name": "East Fort",
        "full_address": "East Fort, Thrissur, Kerala",
        "whatsapp": "919590012678",
        "map_query": "East+Fort+Thrissur+Kerala",
        "hours": "10:00 AM – 10:30 PM",
        "position": 1,
    },
    {
        "id": "westfort",
        "name": "West Fort",
        "full_address": "West Fort Junction, Thrissur, Kerala",
        "whatsapp": "917012611090",
        "map_query": "West+Fort+Thrissur+Kerala",
        "hours": "10:00 AM – 10:30 PM",
        "position": 2,
    },
]
