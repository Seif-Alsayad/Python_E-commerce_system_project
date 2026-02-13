import users
import products
import cart

def main():
    current_user = None

    while True:
        if not current_user:
            # register or login menu
            print("\n=== Welcome to the Python Store ===")
            print("1. Register or Login")
            print("2. Exit Program")
            choice = input("Select an option: ")

            if choice == "1":
                current_user = users.register_or_login()
            elif choice == "2":
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")
        
        else:
            # after user logs in
            print(f"\n--- Hello, {current_user}! ---")
            print("1.Browse Products")
            print("2.Search Products")
            print("3.Add to Cart")
            print("4.Remove from Cart")
            print("5.View Cart & Total")
            print("6.Checkout")
            print("7.View Order History")
            print("8.Logout")
            
            choice = input("Select an option: ")

            if choice == "1":
                products.list_products()
            elif choice == "2":
                products.search_product()
            elif choice == "3":
                cart.add_to_cart(current_user) 
            elif choice == "4":
                cart.remove_from_cart(current_user) 
            elif choice == "5":
                cart.view_cart(current_user) 
            elif choice == "6":
                cart.checkout(current_user)
            elif choice == "7":
                cart.view_history(current_user)
            elif choice == "8":
                print(f"Logging out...")
                current_user = None
            else:
                print("Invalid choice.")

if __name__ == "__main__":
    main()