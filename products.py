import storage

def list_products():
    #Lists all products.
    products = storage.read_file('products.json')
    if not products:
        print("No products available.")
        return
    
    print("Available Products:")
    for product in products:
        print(f"ID: {product.get('product_id')} | {product.get('name')} - ${product.get('price')} - Stock: {product.get('stock')}")


def search_product():

    products = storage.read_file('products.json')

    while True:
        search_term = input("\nEnter product name or ID to search (or type 'back' to cancel): ").strip().lower()
        
        if search_term == 'back': # Allows user to return to the Main Menu
            break

        found_products = [
            p for p in products 
            if search_term in p.get('name', '').lower() or search_term == str(p.get('product_id', ''))
        ]
    
        if not found_products:
            print(f"No products found matching '{search_term}'. Please try again.")
            continue 
    
        print("\nSearch Results:")
        for p in found_products:
             print(f"ID: {p.get('product_id')} | {p.get('name')} - ${p.get('price')} (Stock: {p.get('stock')})")
        break


def check_stock_availability(p_id, requested_qty):
    #Ensure requested quantity doesnt exceed available stock.
    products = storage.read_file('products.json')

    #Find the specific product by ID
    product = next((p for p in products if str(p.get('product_id')) == p_id), None)
    
    if product:
        current_stock = product.get('stock', 0)
        
        if requested_qty <= current_stock:
            return True
        else:
            print(f"Error: Insufficient stock. Only {current_stock} available.")
            return False
    else:
        print("Error: Product not found.")
        return False
    

if __name__ == "__main__":
    list_products()
    search_product()