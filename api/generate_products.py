import random
import json
from datetime import datetime

categories = {
    "Electronics": {
        "Headphone": (1001, 1100, ["boAt", "Sony", "JBL", "Bose", "Noise", "Sennheiser", "Skullcandy", "AKG", "Audio-Technica", "Philips"], (1000, 15000)),
        "Smartphone": (1101, 1200, ["Apple", "Samsung", "OnePlus", "Xiaomi", "POCO", "Realme", "Vivo", "Oppo", "Google", "Motorola"], (8000, 80000)),
        "Laptop": (1201, 1300, ["Dell", "HP", "Lenovo", "Asus", "Acer", "MSI", "Apple", "Microsoft", "Alienware", "Razer"], (20000, 150000)),
        "Tablet": (1301, 1400, ["Apple", "Samsung", "Lenovo", "Microsoft", "Huawei", "Amazon", "Google", "Xiaomi", "Realme", "Oppo"], (10000, 60000)),
        "Smartwatch": (1401, 1500, ["Apple", "Fitbit", "Samsung", "Amazfit", "Garmin", "Xiaomi", "Fossil", "Huawei", "Honor", "Noise"], (1999, 50000)),
    },
    "Home Appliances": {
        "Refrigerator": (2001, 2100, ["LG", "Samsung", "Whirlpool", "Godrej", "Haier", "Bosch", "IFB", "Panasonic", "Sharp", "Hitachi"], (15000, 60000)),
        "Washing Machine": (2101, 2200, ["IFB", "Bosch", "Samsung", "LG", "Whirlpool", "Haier", "Voltas", "Blue Star", "Panasonic", "Godrej"], (12000, 50000)),
        "Air Conditioner": (2201, 2300, ["Daikin", "Voltas", "LG", "Blue Star", "Samsung", "Carrier", "Hitachi", "Panasonic", "Haier", "Sharp"], (25000, 75000)),
        "Microwave": (2301, 2400, ["IFB", "Samsung", "LG", "Panasonic", "Whirlpool", "Godrej", "Bajaj", "Sharp", "Haier", "Bosch"], (3000, 25000)),
    },
    "Fashion": {
        "T-Shirt": (3101, 3200, ["Levi's", "U.S. Polo", "Zara", "H&M", "Nike", "Adidas", "Puma", "Calvin Klein", "Tommy Hilfiger", "Ralph Lauren"], (300, 5000)),
        "Jeans": (3201, 3300, ["Levi's", "Wrangler", "Lee", "Pepe", "Calvin Klein", "Tommy Hilfiger", "Gap", "Diesel", "True Religion", "G-Star Raw"], (800, 10000)),
        "Sneakers": (3301, 3400, ["Nike", "Adidas", "Puma", "Reebok", "Converse", "Vans", "New Balance", "ASICS", "Skechers", "Under Armour"], (1000, 15000)),
        "Handbag": (3401, 3500, ["Gucci", "Louis Vuitton", "Coach", "Michael Kors", "Prada", "Chanel", "Fendi", "Burberry", "Tory Burch", "Kate Spade"], (500, 50000)),
        "Jacket": (3501, 3600, ["North Face", "Adidas", "Puma", "Columbia", "Nike", "Under Armour", "Patagonia", "Arc'teryx", "Moncler", "Canada Goose"], (1500, 15000)),
    },
    "Beauty": {
        "Perfume": (4001, 4100, ["Chanel", "Dior", "Gucci", "Versace", "Tom Ford", "Yves Saint Laurent", "Prada", "Burberry", "Calvin Klein", "Jean Paul Gaultier"], (250, 3000)),
        "Lipstick": (4101, 4200, ["MAC", "Maybelline", "L'Oreal", "Revlon", "Lakme", "Colorbar", "Faces Canada", "NYX", "Bobbi Brown", "SUGAR"], (300, 3000)),
        "Foundation": (4201, 4300, ["Maybelline", "L'Oreal", "Revlon", "MAC", "Lakme", "Faces Canada", "Bobbi Brown", "SUGAR", "Colorbar", "Estee Lauder"], (300, 5000)),
        "Hair Dryer": (4301, 4400, ["Philips", "Panasonic", "Havells", "Syska", "Braun", "Vidal Sassoon", "Remington", "Nova", "Wahl", "Dyson"], (800, 10000)),
        "Shampoo": (4401, 4500, ["Dove", "Head & Shoulders", "Pantene", "Garnier", "L'Oreal", "TRESemmé", "Sunsilk", "Matrix", "Herbal Essences", "Himalaya"], (200, 1000)),
    },
    "Furniture": {
        "Sofa": (5001, 5100, ["IKEA", "Ashley", "La-Z-Boy", "Godrej", "Urban Ladder", "Home Centre", "Hometown", "Nilkamal", "Durian", "Royaloak"], (20000, 200000)),
        "Bed": (5101, 5200, ["IKEA", "Durian", "Springfit", "Wakefit", "Godrej", "Urban Ladder", "Home Centre", "Hometown", "Royaloak", "Sleepwell"], (8000, 100000)),
        "Dining Table": (5201, 5300, ["IKEA", "Godrej", "Urban Ladder", "Home Centre", "Hometown", "Nilkamal", "Royaloak", "Wood World", "Style Spa", "Furniturewalla"], (5000, 10000)),
        "Chair": (5301, 5400, ["IKEA", "Godrej", "Urban Ladder", "Home Centre", "Hometown", "Nilkamal", "Royaloak", "Featherlite", "HOF", "Herman Miller"], (1000, 30000)),
        "Wardrobe": (5401, 5500, ["IKEA", "Godrej", "Urban Ladder", "Home Centre", "Hometown", "Nilkamal", "Spacewood", "Royaloak", "Style Spa", "Zuari"], (10000, 150000)),
    },
    "Books": {
        "Fiction": (6001, 6100, ["Penguin", "HarperCollins", "Simon & Schuster", "Random House", "Hachette", "Pan Macmillan", "Bloomsbury", "Scholastic", "Tor Books", "Bantam"], (200, 1500)),
        "Non-Fiction": (6101, 6200, ["Penguin", "Hachette", "Macmillan", "Oxford", "Cambridge", "Wiley", "Pearson", "MIT Press", "National Geographic", "Simon & Schuster"], (300, 2000)),
        "Academic": (6201, 6300, ["Pearson", "Wiley", "Oxford", "Cambridge", "McGraw-Hill", "Cengage", "Routledge", "SAGE", "Elsevier", "Springer"], (500, 5000)),
        "Comics": (6301, 6400, ["Marvel", "DC", "Image Comics", "Dark Horse", "IDW Publishing", "Boom! Studios", "Valiant", "Manga", "Top Shelf", "Fantagraphics"], (150, 2000)),
    },
}

def generate_product_name(category, subcategory, brand):
    if category == "Electronics":
        if subcategory == "Headphone":
            return f"{brand} {random.choice(['Wireless', 'Bluetooth', 'Noise Cancelling', 'Gaming', 'Sports'])} {subcategory}"
        elif subcategory == "Smartphone":
            return f"{brand} {random.choice(['Pro', 'Max', 'Plus', 'Ultra', 'Lite'])} {random.randint(1, 20)}"
        elif subcategory == "Laptop":
            return f"{brand} {random.choice(['Pro', 'Air', 'Gaming', 'Business', 'Student'])} {random.randint(1, 20)}"
        elif subcategory == "Tablet":
            return f"{brand} {random.choice(['Pro', 'Air', 'Mini', 'Plus', 'Ultra'])} {random.randint(1, 10)}"
        elif subcategory == "Smartwatch":
            return f"{brand} {random.choice(['Pro', 'Active', 'Fitness', 'Classic', 'Sport'])} {random.randint(1, 5)}"
    elif category == "Home Appliances":
        if subcategory == "Refrigerator":
            return f"{brand} {random.choice(['Frost Free', 'Double Door', 'Side by Side', 'French Door', 'Smart'])} {subcategory}"
        elif subcategory == "Washing Machine":
            return f"{brand} {random.choice(['Front Load', 'Top Load', 'Semi-Automatic', 'Fully Automatic', 'Smart'])} {subcategory}"
        elif subcategory == "Air Conditioner":
            return f"{brand} {random.choice(['Split', 'Window', 'Inverter', 'Smart', 'Premium'])} {subcategory}"
        elif subcategory == "Microwave":
            return f"{brand} {random.choice(['Convection', 'Grill', 'Solo', 'Smart', 'Premium'])} {subcategory}"
    elif category == "Fashion":
        if subcategory == "T-Shirt":
            return f"{brand} {random.choice(['Classic', 'Sport', 'Graphic', 'Premium', 'Basic'])} {subcategory}"
        elif subcategory == "Jeans":
            return f"{brand} {random.choice(['Slim Fit', 'Regular Fit', 'Skinny', 'Relaxed', 'Straight'])} {subcategory}"
        elif subcategory == "Sneakers":
            return f"{brand} {random.choice(['Running', 'Training', 'Lifestyle', 'Basketball', 'Football'])} {subcategory}"
        elif subcategory == "Handbag":
            return f"{brand} {random.choice(['Tote', 'Shoulder', 'Crossbody', 'Clutch', 'Backpack'])} {subcategory}"
        elif subcategory == "Jacket":
            return f"{brand} {random.choice(['Winter', 'Rain', 'Sports', 'Casual', 'Premium'])} {subcategory}"
    elif category == "Beauty":
        if subcategory == "Perfume":
            return f"{brand} {random.choice(['Eau de Parfum', 'Eau de Toilette', 'Eau de Cologne', 'Pure', 'Premium'])}"
        elif subcategory == "Lipstick":
            return f"{brand} {random.choice(['Matte', 'Glossy', 'Satin', 'Liquid', 'Long Lasting'])} {subcategory}"
        elif subcategory == "Foundation":
            return f"{brand} {random.choice(['Matte', 'Dewy', 'Long Lasting', 'Full Coverage', 'Natural'])} {subcategory}"
        elif subcategory == "Hair Dryer":
            return f"{brand} {random.choice(['Professional', 'Travel', 'Ionic', 'Ceramic', 'Smart'])} {subcategory}"
        elif subcategory == "Shampoo":
            return f"{brand} {random.choice(['Daily Care', 'Repair', 'Volume', 'Color Protect', 'Natural'])} {subcategory}"
    elif category == "Furniture":
        if subcategory == "Sofa":
            return f"{brand} {random.choice(['3 Seater', '2 Seater', 'L-Shape', 'Recliner', 'Premium'])} {subcategory}"
        elif subcategory == "Bed":
            return f"{brand} {random.choice(['Queen', 'King', 'Single', 'Double', 'Premium'])} {subcategory}"
        elif subcategory == "Dining Table":
            return f"{brand} {random.choice(['4 Seater', '6 Seater', '8 Seater', 'Extendable', 'Premium'])} {subcategory}"
        elif subcategory == "Chair":
            return f"{brand} {random.choice(['Office', 'Gaming', 'Dining', 'Recliner', 'Premium'])} {subcategory}"
        elif subcategory == "Wardrobe":
            return f"{brand} {random.choice(['Sliding', 'Hinged', 'Walk-in', 'Built-in', 'Premium'])} {subcategory}"
    elif category == "Books":
        if subcategory == "Fiction":
            return f"{brand} {random.choice(['Classic', 'Contemporary', 'Bestseller', 'Award-winning', 'Premium'])} {subcategory}"
        elif subcategory == "Non-Fiction":
            return f"{brand} {random.choice(['Biography', 'History', 'Science', 'Business', 'Premium'])} {subcategory}"
        elif subcategory == "Academic":
            return f"{brand} {random.choice(['Textbook', 'Reference', 'Study Guide', 'Workbook', 'Premium'])} {subcategory}"
        elif subcategory == "Comics":
            return f"{brand} {random.choice(['Graphic Novel', 'Collection', 'Special Edition', 'Limited', 'Premium'])} {subcategory}"
    
    return f"{brand} {subcategory}"

def generate_description(category, subcategory, brand):
    descriptions = {
        "Electronics": {
            "Headphone": f"High-quality {brand} {subcategory} with premium sound quality and comfortable design.",
            "Smartphone": f"Latest {brand} {subcategory} with advanced features and powerful performance.",
            "Laptop": f"Powerful {brand} {subcategory} for work and entertainment.",
            "Tablet": f"Versatile {brand} {subcategory} for productivity and entertainment.",
            "Smartwatch": f"Smart {brand} {subcategory} with fitness tracking and notifications."
        },
        "Home Appliances": {
            "Refrigerator": f"Energy-efficient {brand} {subcategory} with advanced cooling technology.",
            "Washing Machine": f"Smart {brand} {subcategory} with multiple wash programs.",
            "Air Conditioner": f"Powerful {brand} {subcategory} with energy-saving features.",
            "Microwave": f"Convenient {brand} {subcategory} with multiple cooking modes."
        },
        "Fashion": {
            "T-Shirt": f"Comfortable {brand} {subcategory} made from premium materials.",
            "Jeans": f"Stylish {brand} {subcategory} with perfect fit and durability.",
            "Sneakers": f"Comfortable {brand} {subcategory} for everyday wear.",
            "Handbag": f"Elegant {brand} {subcategory} with premium materials.",
            "Jacket": f"Stylish {brand} {subcategory} for all weather conditions."
        },
        "Beauty": {
            "Perfume": f"Luxurious {brand} {subcategory} with long-lasting fragrance.",
            "Lipstick": f"Long-lasting {brand} {subcategory} with rich color.",
            "Foundation": f"Natural-looking {brand} {subcategory} with full coverage.",
            "Hair Dryer": f"Professional {brand} {subcategory} with multiple heat settings.",
            "Shampoo": f"Gentle {brand} {subcategory} for healthy hair."
        },
        "Furniture": {
            "Sofa": f"Comfortable {brand} {subcategory} with premium upholstery.",
            "Bed": f"Stylish {brand} {subcategory} with comfortable mattress.",
            "Dining Table": f"Elegant {brand} {subcategory} for family gatherings.",
            "Chair": f"Ergonomic {brand} {subcategory} for maximum comfort.",
            "Wardrobe": f"Spacious {brand} {subcategory} with multiple compartments."
        },
        "Books": {
            "Fiction": f"Engaging {brand} {subcategory} with compelling storyline.",
            "Non-Fiction": f"Informative {brand} {subcategory} with detailed insights.",
            "Academic": f"Comprehensive {brand} {subcategory} for students.",
            "Comics": f"Entertaining {brand} {subcategory} with vibrant illustrations."
        }
    }
    return descriptions.get(category, {}).get(subcategory, f"Quality {brand} {subcategory}.")

def generate_products():
    products = []
    
    for category, subcategories in categories.items():
        for subcategory, (start_id, end_id, brands, (min_price, max_price)) in subcategories.items():
            # Generate 5 products for each subcategory
            for _ in range(5):
                brand = random.choice(brands)
                product_id = random.randint(start_id, end_id)
                base_price = random.randint(min_price, max_price)
                current_price = int(base_price * random.uniform(0.8, 1.2))  # 20% variation
                min_price = int(base_price * 0.7)  # 30% below base price
                max_price = int(base_price * 1.3)  # 30% above base price
                target_margin = random.uniform(0.1, 0.3)  # 10-30% margin
                
                product = {
                    "id": product_id,
                    "name": generate_product_name(category, subcategory, brand),
                    "description": generate_description(category, subcategory, brand),
                    "base_price": base_price,
                    "current_price": current_price,
                    "category": category,
                    "subcategory": subcategory,
                    "brand": brand,
                    "url": f"https://www.amazon.in/dummy-product-{product_id}",
                    "min_price": min_price,
                    "max_price": max_price,
                    "target_margin": target_margin,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                }
                products.append(product)
    
    return products

# Generate products and save to JSON file
products = generate_products()
with open('dummy_products.json', 'w') as f:
    json.dump(products, f, indent=2)

print(f"Generated {len(products)} dummy products") 