import json

def load_inventory(filename="store_data.json"):
    with open(filename, "r") as f:
        return json.load(f)

def save_inventory(inventory, filename="store_data.json"):
    with open(filename, "w") as f:
        json.dump(inventory, f, indent=4)

def display_sections(inventory):
    print("\nAvailable Sections:")
    for section in inventory.keys():
        print(f" - {section}")

def display_items(inventory, section):
    print(f"\nItems in {section}:")
    for item, data in inventory[section].items():
        print(f"  {item} - {data['qty']} available - Rs. {data['price']} each")

def shopping_session():
    try:
        inventory = load_inventory()
    except (FileNotFoundError, json.JSONDecodeError):
        print("❌ Error: store_data.json is missing or has invalid JSON.")
        return

    customer_name = input("\nEnter customer name: ").strip().title()
    print(f"\n--- Welcome to the Departmental Store, {customer_name}! ---")

    cart = {}

    while True:
        display_sections(inventory)
        section_input = input("\nEnter section name (or 'done' to checkout): ").strip()
        if section_input.lower() == "done":
            break

        # Case-insensitive section matching
        section = None
        for sec in inventory:
            if sec.lower() == section_input.lower():
                section = sec
                break
        if not section:
            print("❌ Section not found.")
            continue

        display_items(inventory, section)
        item_input = input("Enter item name: ").strip()

        # Case-insensitive item matching
        item = None
        for itm in inventory[section]:
            if itm.lower() == item_input.lower():
                item = itm
                break
        if not item:
            print("❌ Item not found in this section.")
            continue

        try:
            quantity = int(input("Enter quantity: "))
            if quantity <= 0:
                print("❌ Quantity must be positive.")
                continue
        except ValueError:
            print("❌ Please enter a valid number.")
            continue

        if inventory[section][item]['qty'] < quantity:
            print("❌ Out of stock or insufficient quantity.")
            continue

        # Add to cart and reduce inventory stock
        price = inventory[section][item]['price']
        if item not in cart:
            cart[item] = {"qty": 0, "price": price}
        cart[item]["qty"] += quantity
        inventory[section][item]['qty'] -= quantity
        print(f"✅ {quantity} {item}(s) added to cart.")

    # Checkout
    print("\n--- Checkout ---")
    if cart:
        total = 0
        print(f"\nBill for {customer_name}:")
        for item, details in cart.items():
            line_total = details["qty"] * details["price"]
            print(f"  {item} - {details['qty']} × Rs. {details['price']} = Rs. {line_total}")
            total += line_total
        print(f"\nTotal Bill: Rs. {total}")
    else:
        print("No items purchased.")

    save_inventory(inventory)
    print("\nThank you for shopping with us!")

if __name__ == "__main__":
    while True:
        shopping_session()
        cont = input("\nNext customer? (yes/no): ").lower()
        if cont != "yes":
            print("\nStore Closed. Have a great day!")
            break