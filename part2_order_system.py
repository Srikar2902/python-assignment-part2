import copy

# ==========================================================
# PROVIDED DATA
# ==========================================================
menu = {
    "Paneer Tikka":   {"category": "Starters",  "price": 180.0, "available": True},
    "Chicken Wings":  {"category": "Starters",  "price": 220.0, "available": False},
    "Veg Soup":       {"category": "Starters",  "price": 120.0, "available": True},
    "Butter Chicken": {"category": "Mains",     "price": 320.0, "available": True},
    "Dal Tadka":      {"category": "Mains",     "price": 180.0, "available": True},
    "Veg Biryani":    {"category": "Mains",     "price": 250.0, "available": True},
    "Garlic Naan":    {"category": "Mains",     "price":  40.0, "available": True},
    "Gulab Jamun":    {"category": "Desserts",  "price":  90.0, "available": True},
    "Rasgulla":       {"category": "Desserts",  "price":  80.0, "available": True},
    "Ice Cream":      {"category": "Desserts",  "price": 110.0, "available": False},
}

inventory = {
    "Paneer Tikka":   {"stock": 10, "reorder_level": 3},
    "Chicken Wings":  {"stock":  8, "reorder_level": 2},
    "Veg Soup":       {"stock": 15, "reorder_level": 5},
    "Butter Chicken": {"stock": 12, "reorder_level": 4},
    "Dal Tadka":      {"stock": 20, "reorder_level": 5},
    "Veg Biryani":    {"stock":  6, "reorder_level": 3},
    "Garlic Naan":    {"stock": 30, "reorder_level": 10},
    "Gulab Jamun":    {"stock":  5, "reorder_level": 2},
    "Rasgulla":       {"stock":  4, "reorder_level": 3},
    "Ice Cream":      {"stock":  7, "reorder_level": 4},
}

sales_log = {
    "2025-01-01": [
        {"order_id": 1,  "items": ["Paneer Tikka", "Garlic Naan"],          "total": 220.0},
        {"order_id": 2,  "items": ["Gulab Jamun", "Veg Soup"],              "total": 210.0},
        {"order_id": 3,  "items": ["Butter Chicken", "Garlic Naan"],        "total": 360.0},
    ],
    "2025-01-02": [
        {"order_id": 4,  "items": ["Dal Tadka", "Garlic Naan"],             "total": 220.0},
        {"order_id": 5,  "items": ["Veg Biryani", "Gulab Jamun"],           "total": 340.0},
    ],
    "2025-01-03": [
        {"order_id": 6,  "items": ["Paneer Tikka", "Rasgulla"],             "total": 260.0},
        {"order_id": 7,  "items": ["Butter Chicken", "Veg Biryani"],        "total": 570.0},
        {"order_id": 8,  "items": ["Garlic Naan", "Gulab Jamun"],           "total": 130.0},
    ],
    "2025-01-04": [
        {"order_id": 9,  "items": ["Dal Tadka", "Garlic Naan", "Rasgulla"], "total": 300.0},
        {"order_id": 10, "items": ["Paneer Tikka", "Gulab Jamun"],          "total": 270.0},
    ],
}

# ==========================================================
# Task 1: Explore the Menu
# ==========================================================
# Justification: Grouping by category improves user experience. 
# I'm using a set to find unique categories first.
print("--- Task 1: Menu Exploration ---")
categories = ["Starters", "Mains", "Desserts"]

for cat in categories:
    print(f"\n===== {cat} =====")
    for item, details in menu.items():
        if details["category"] == cat:
            status = "Available" if details["available"] else "Unavailable"
            print(f"{item:<18} ₹{details['price']:>6.2f}   [{status}]")

# Quick Stats
total_items = len(menu)
available_items = sum(1 for item in menu.values() if item["available"])
most_expensive = max(menu, key=lambda x: menu[x]["price"])
cheap_items = [name for name, d in menu.items() if d["price"] < 150]

print(f"\nTotal Menu Items: {total_items}")
print(f"Available Items : {available_items}")
print(f"Most Expensive  : {most_expensive} (₹{menu[most_expensive]['price']})")
print(f"Items under ₹150: {', '.join(cheap_items)}\n")


# ==========================================================
# Task 2: Cart Operations
# ==========================================================
# Justification: Using a list of dictionaries for the cart allows us 
# to easily store 'item', 'quantity', and 'price' as a single object.
cart = []

def update_cart(item_name, qty_change):
    # Check if item exists and is available in menu
    if item_name not in menu:
        print(f"Error: '{item_name}' is not on the menu.")
        return
    if not menu[item_name]["available"]:
        print(f"Error: '{item_name}' is currently unavailable.")
        return
    
    # Logic to update quantity if already in cart
    for entry in cart:
        if entry["item"] == item_name:
            entry["quantity"] += qty_change
            return
            
    # If not in cart, add new entry
    cart.append({"item": item_name, "quantity": qty_change, "price": menu[item_name]["price"]})

# Simulation Sequence
print("--- Task 2: Simulating Orders ---")
update_cart("Paneer Tikka", 2)
update_cart("Gulab Jamun", 1)
update_cart("Paneer Tikka", 1) # Should update Qty to 3
update_cart("Mystery Burger", 1) # Invalid
update_cart("Chicken Wings", 1) # Unavailable

# Removing an item
for i in range(len(cart)):
    if cart[i]["item"] == "Gulab Jamun":
        del cart[i]
        break

# Order Summary Calculation
print("\n========== Order Summary ==========")
subtotal = 0
for entry in cart:
    total_item_price = entry['quantity'] * entry['price']
    subtotal += total_item_price
    print(f"{entry['item']:<18} x{entry['quantity']}   ₹{total_item_price:>7.2f}")

gst = subtotal * 0.05
print("-" * 35)
print(f"Subtotal:                ₹{subtotal:>7.2f}")
print(f"GST (5%):                ₹{gst:>7.2f}")
print(f"Total Payable:           ₹{subtotal + gst:>7.2f}")
print("====================================\n")


# ==========================================================
# Task 3: Inventory Tracker with Deep Copy
# ==========================================================
# Justification: Deep copy is essential because these are nested dictionaries. 
# A normal copy would still link the inner dictionaries together.
inventory_backup = copy.deepcopy(inventory)

# Demonstration of Deep Copy
inventory["Paneer Tikka"]["stock"] = 99
# Restoration (Manual demonstration)
inventory["Paneer Tikka"]["stock"] = 10 

print("--- Task 3: Inventory Fulfilment ---")
# Deducting cart items from stock
for entry in cart:
    item = entry["item"]
    ordered_qty = entry["quantity"]
    
    if item in inventory:
        current_stock = inventory[item]["stock"]
        if current_stock < ordered_qty:
            print(f"Warning: Insufficient stock for {item}. Deducting only {current_stock}.")
            inventory[item]["stock"] = 0
        else:
            inventory[item]["stock"] -= ordered_qty

# Reorder Alerts
for item, info in inventory.items():
    if info["stock"] <= info["reorder_level"]:
        print(f"⚠ Reorder Alert: {item} — Only {info['stock']} left (level: {info['reorder_level']})")


# ==========================================================
# Task 4: Daily Sales Log Analysis
# ==========================================================
# Justification: I'm using a nested loop to traverse days and then 
# individual orders to get the full picture of sales.
print("\n--- Task 4: Sales Analysis ---")

# Add new day
sales_log["2025-01-05"] = [
    {"order_id": 11, "items": ["Butter Chicken", "Gulab Jamun", "Garlic Naan"], "total": 490.0},
    {"order_id": 12, "items": ["Paneer Tikka", "Rasgulla"], "total": 260.0},
]

best_day = ""
max_revenue = 0
item_counts = {}

print(f"{'Date':<12} | {'Revenue'}")
print("-" * 25)

for date, orders in sales_log.items():
    daily_total = sum(o["total"] for o in orders)
    print(f"{date:<12} | ₹{daily_total:>7.2f}")
    
    if daily_total > max_revenue:
        max_revenue = daily_total
        best_day = date
        
    for o in orders:
        for item in o["items"]:
            item_counts[item] = item_counts.get(item, 0) + 1

most_ordered = max(item_counts, key=item_counts.get)
print("-" * 25)
print(f"Best Selling Day: {best_day}")
print(f"Most Ordered Item: {most_ordered} ({item_counts[most_ordered]} orders)")

print("\n--- Full Order History ---")
counter = 1
for date, orders in sales_log.items():
    for o in orders:
        print(f"{counter}. [{date}] Order #{o['order_id']} — ₹{o['total']:.2f} — Items: {', '.join(o['items'])}")
        counter += 1