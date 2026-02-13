import storage
import products
import datetime
import uuid

# Cart management functions
# makes sure carts are persisted in 'carts.json' with username.

def get_all_carts():
    return storage.read_file('carts.json')

def save_all_carts(all_carts):
    storage.save_to_file(all_carts, 'carts.json')

def get_user_cart(username):
    all_carts = get_all_carts()
    if isinstance(all_carts, list):
        return []
    return all_carts.get(username, [])

def update_user_cart(username, cart_data):
    all_carts = get_all_carts()
    if isinstance(all_carts, list):
        all_carts = {}
    all_carts[username] = cart_data
    save_all_carts(all_carts)

def add_to_cart(username):
    #promts the user to enter the ID of the product they want to buy and the quantity.
    p_id = input("Enter the Product ID you want to buy: ").strip()

    #validates the quantity input and checks if the requested quantity is available in stock before adding to cart.
    try:
        qty = int(input("Enter quantity: "))
        if qty <= 0:
            print("Quantity must be greater than zero.")
            return

        if products.check_stock_availability(p_id, qty):
            all_products = storage.read_file('products.json')
            product = next((p for p in all_products if str(p.get('product_id')) == p_id), None)
            
            if product:
                user_cart = get_user_cart(username)
                item_exists = False
                for item in user_cart: #if the item already exists in cart, it updates the quantity instead of adding a duplicate.
                    if item['product_id'] == p_id:
                        item['quantity'] += qty
                        item_exists = True
                        break
                
                if not item_exists:
                    user_cart.append({
                        "product_id": p_id,
                        "name": product['name'],
                        "price": product['price'], #
                        "quantity": qty
                    })
                update_user_cart(username, user_cart)
                print(f"Added {qty} x {product['name']} to your cart.")
            else:
                print("Error: Product details could not be retrieved.")
    except ValueError:
        print("Invalid input. Please enter a number for quantity.")

def remove_from_cart(username):
    user_cart = get_user_cart(username)
    if not user_cart:
        print("\nYour cart is empty.")
        return

    #promts the user to enter the ID of the item to remove or reduce quantity.
    p_id = input("Enter the Product ID you want to remove/reduce: ").strip()
    item_to_update = next((item for item in user_cart if str(item.get('product_id')) == p_id), None)
            
    if not item_to_update:
        print("Error: Product ID not found in your cart.")
        return

    print(f"Current quantity of {item_to_update['name']}: {item_to_update['quantity']}")
    
    #asks the user how many to remove.
    try:
        remove_qty = int(input(f"How many would you like to remove? "))
        if remove_qty <= 0:
            print("Quantity to remove must be greater than zero.")
            return

        if remove_qty >= item_to_update['quantity']:
            user_cart.remove(item_to_update)
            print(f"Removed {item_to_update['name']} completely from cart.")
        else:
            item_to_update['quantity'] -= remove_qty
            print(f"Reduced {item_to_update['name']} quantity. New quantity: {item_to_update['quantity']}")
        
        update_user_cart(username, user_cart)
            
    except ValueError:
        print("Invalid input. Please enter a number.")

def view_history(username):
    #fetches all orders from 'orders.json' and filters them by the current username to display order history.
    all_orders = storage.read_file('orders.json')
    user_orders = [o for o in all_orders if o.get('username') == username]

    if not user_orders:
        print("\nNo order history found for your account.")
        return

    print(f"\n=== Order History ===")
    for order in user_orders:
        print(f"Order ID: {order['order_id']} | Date: {order['timestamp']}")
        print(f"Total: ${order['total_paid']:.2f}")
        print("Items:")
        for item in order['items']:
            print(f"  - {item['name']} (x{item['quantity']}) @ ${item['price']:.2f} ea")
        print("==================")

def view_cart(username):
    user_cart = get_user_cart(username)
    if not user_cart:
        print("\nYour cart is empty.")
        return

    #displays the contents of the user's cart along with the total balance.
    print("\n--- Your Shopping Cart ---")
    total = 0
    for item in user_cart:
        subtotal = item['price'] * item['quantity']
        total += subtotal
        print(f"{item['name']} - Qty: {item['quantity']} | Unit Price: ${item['price']:.2f} | Subtotal: ${subtotal:.2f}")
    
    print(f"--- Total Balance: ${total:.2f} ---")

def checkout(username):
    user_cart = get_user_cart(username)
    if not user_cart:
        print("Nothing to checkout. Your cart is empty.")
        return

    all_products = storage.read_file('products.json')
    total_bill = 0
    
    #validate stock availability for all items in the cart.
    for cart_item in user_cart:
        product = next((p for p in all_products if str(p.get('product_id')) == cart_item['product_id']), None)
        if not product:
            print(f"Error: {cart_item['name']} no longer exists in our catalog.")
            return
        if product['stock'] < cart_item['quantity']:
            print(f"Checkout Failed: '{product['name']}' only has {product['stock']} left.")
            return

    #deduct stock and calculate total bill.
    for cart_item in user_cart:
        for p in all_products:
            if str(p.get('product_id')) == cart_item['product_id']:
                p['stock'] -= cart_item['quantity']
                total_bill += cart_item['price'] * cart_item['quantity']
                break

    storage.save_to_file(all_products, 'products.json')

    #record the order
    order_data = {
        "order_id": str(uuid.uuid4())[:8],
        "username": username,
        "items": user_cart,
        "total_paid": total_bill,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    storage.append_to_file(order_data, 'orders.json')

    #generate receipt in txt file.
    receipt_filename = f"receipt_{order_data['order_id']}.txt"
    with open(receipt_filename, "w") as f:
        f.write(f"ORDER RECEIPT\n")
        f.write(f"==========================\n")
        f.write(f"Order ID: {order_data['order_id']}\n") 
        f.write(f"Customer: {username}\n") 
        f.write(f"Date: {order_data['timestamp']}\n") 
        f.write(f"--------------------------\n")
        for item in user_cart:
            f.write(f"{item['name']} x{item['quantity']} at ${item['price']:.2f}\n") 
        f.write(f"--------------------------\n")
        f.write(f"TOTAL PAID: ${total_bill:.2f}\n") 
        f.write(f"==========================\n")
        f.write(f"Thank you for shopping")
    
    print(f"\ncheckout successful! order ID: {order_data['order_id']}")
    print(f"receipt exported to {receipt_filename}")
    
    update_user_cart(username, [])