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

# --- Task 1: Explore the Menu ---
print("--- Task 1: Menu Exploration ---")
categories = ["Starters", "Mains", "Desserts"]
for cat in categories:
    print(f"\n===== {cat} =====")
    for item, details in menu.items():
        if details["category"] == cat:
            status = "Available" if details["available"] else "Unavailable"
            print(f"{item:<18} ₹{details['price']:>6.2f}   [{status}]")

# Menu Stats
print(f"\nTotal Menu Items: {len(menu)}")
print(f"Available Items : {sum(1 for i in menu.values() if i['available'])}")
most_exp = max(menu, key=lambda x: menu[x]["price"])
print(f"Most Expensive  : {most_exp} (₹{menu[most_exp]['price']})")
cheap_list = [n for n, d in menu.items() if d["price"] < 150]
print(f"Items under ₹150: {', '.join(cheap_list)}\n")

# --- Task 2: Cart Operations ---
cart = []
def add_to_cart(item, qty):
    if item not in menu:
        print(f"Error: '{item}' is not on the menu.")
        return
    if not menu[item]["available"]:
        print(f"Error: '{item}' is currently unavailable.")
        return
    for entry in cart:
        if entry["item"] == item:
            entry["quantity"] += qty
            return
    cart.append({"item": item, "quantity": qty, "price": menu[item]["price"]})

print("--- Task 2: Simulating Orders ---")
add_to_cart("Paneer Tikka", 2)
add_to_cart("Gulab Jamun", 1)
add_to_cart("Paneer Tikka", 1)
add_to_cart("Mystery Burger", 1)
add_to_cart("Chicken Wings", 1)

# Removing item
for i in range(len(cart)):
    if cart[i]["item"] == "Gulab Jamun":
        del cart[i]
        break

print("\n========== Order Summary ==========")
subtotal = sum(e["quantity"] * e["price"] for e in cart)
for e in cart:
    print(f"{e['item']:<18} x{e['quantity']}   ₹{e['quantity']*e['price']:>7.2f}")
gst = subtotal * 0.05
print("-" * 35)
print(f"Subtotal:                ₹{subtotal:>7.2f}")
print(f"GST (5%):                ₹{gst:>7.2f}")
print(f"Total Payable:           ₹{subtotal + gst:>7.2f}")
print("====================================\n")

# --- Task 3: Inventory Tracker ---
inventory_backup = copy.deepcopy(inventory)
# Fulfilment
for e in cart:
    item = e["item"]
    if item in inventory:
        if inventory[item]["stock"] >= e["quantity"]:
            inventory[item]["stock"] -= e["quantity"]
        else:
            inventory[item]["stock"] = 0

print("--- Task 3: Inventory Fulfilment ---")
for item, info in inventory.items():
    if info["stock"] <= info["reorder_level"]:
        print(f"⚠ Reorder Alert: {item} — Only {info['stock']} left (level: {info['reorder_level']})")

# --- Task 4: Sales Analysis ---
sales_log["2025-01-05"] = [
    {"order_id": 11, "items": ["Butter Chicken", "Gulab Jamun", "Garlic Naan"], "total": 490.0},
    {"order_id": 12, "items": ["Paneer Tikka", "Rasgulla"], "total": 260.0},
]

print("\n--- Task 4: Sales Analysis ---")
daily_revs = {d: sum(o["total"] for o in ords) for d, ords in sales_log.items()}
print(f"{'Date':<12} | {'Revenue'}")
print("-" * 25)
for d, r in daily_revs.items():
    print(f"{d:<12} | ₹{r:>7.2f}")

best_day = max(daily_revs, key=daily_revs.get)
print("-" * 25)
print(f"Best Selling Day: {best_day}")

# --- Full Order History ---
print("\n--- Full Order History ---")
idx = 1
for d, ords in sales_log.items():
    for o in ords:
        print(f"{idx}. [{d}] Order #{o['order_id']} — ₹{o['total']:.2f} — Items: {', '.join(o['items'])}")
        idx += 1

"""
==========================================================
OFFICIAL PROGRAM OUTPUT (VERIFIED IN VS CODE)
==========================================================
srikarmuppala@Srikars-Laptop / % /usr/local/bin/python3 "/Users/srikarmuppala/Documents/ Business Analytics BITSOM/Assignments/Module 3 assignment/Part 2 Data Structures/import copy.py"
--- Task 1: Menu Exploration ---

===== Starters =====
Paneer Tikka       ₹180.00   [Available]
Chicken Wings      ₹220.00   [Unavailable]
Veg Soup           ₹120.00   [Available]

===== Mains =====
Butter Chicken     ₹320.00   [Available]
Dal Tadka          ₹180.00   [Available]
Veg Biryani        ₹250.00   [Available]
Garlic Naan        ₹ 40.00   [Available]

===== Desserts =====
Gulab Jamun        ₹ 90.00   [Available]
Rasgulla           ₹ 80.00   [Available]
Ice Cream          ₹110.00   [Unavailable]

Total Menu Items: 10
Available Items : 8
Most Expensive  : Butter Chicken (₹320.0)
Items under ₹150: Veg Soup, Garlic Naan, Gulab Jamun, Rasgulla, Ice Cream

--- Task 2: Simulating Orders ---
Error: 'Mystery Burger' is not on the menu.
Error: 'Chicken Wings' is currently unavailable.

========== Order Summary ==========
Paneer Tikka       x3   ₹ 540.00
-----------------------------------
Subtotal:                ₹ 540.00
GST (5%):                ₹  27.00
Total Payable:           ₹ 567.00
====================================

--- Task 3: Inventory Fulfilment ---

--- Task 4: Sales Analysis ---
Date         | Revenue
-------------------------
2025-01-01   | ₹ 790.00
2025-01-02   | ₹ 560.00
2025-01-03   | ₹ 960.00
2025-01-04   | ₹ 570.00
2025-01-05   | ₹ 750.00
-------------------------
Best Selling Day: 2025-01-03

--- Full Order History ---
1. [2025-01-01] Order #1 — ₹220.00 — Items: Paneer Tikka, Garlic Naan
2. [2025-01-01] Order #2 — ₹210.00 — Items: Gulab Jamun, Veg Soup
3. [2025-01-01] Order #3 — ₹360.00 — Items: Butter Chicken, Garlic Naan
4. [2025-01-02] Order #4 — ₹220.00 — Items: Dal Tadka, Garlic Naan
5. [2025-01-02] Order #5 — ₹340.00 — Items: Veg Biryani, Gulab Jamun
6. [2025-01-03] Order #6 — ₹260.00 — Items: Paneer Tikka, Rasgulla
7. [2025-01-03] Order #7 — ₹570.00 — Items: Butter Chicken, Veg Biryani
8. [2025-01-03] Order #8 — ₹130.00 — Items: Garlic Naan, Gulab Jamun
9. [2025-01-04] Order #9 — ₹300.00 — Items: Dal Tadka, Garlic Naan, Rasgulla
10. [2025-01-04] Order #10 — ₹270.00 — Items: Paneer Tikka, Gulab Jamun
11. [2025-01-05] Order #11 — ₹490.00 — Items: Butter Chicken, Gulab Jamun, Garlic Naan
12. [2025-01-05] Order #12 — ₹260.00 — Items: Paneer Tikka, Rasgulla
srikarmuppala@Srikars-Laptop / % 
==========================================================
"""