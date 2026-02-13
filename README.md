# Mini-Amazon E-Commerce System

Console-based e-commerce platform built in Python. This system allows users to browse products, manage a persistent shopping cart, and perform checkouts with inventory management.

## Project Structure
The system is built using a modular design with clear separation of concerns:
* `main.py`: The entry point of the program containing the menu interface.
* `users.py`: Handles user registration and authentication.
* `products.py`: Manages products, search, and stock availability checks.
* `products.json`: Example products for the system to use.
* `cart.py`: Manages cart operations, checkout, and order history.
* `storage.py`: A helper module for JSON file reading, writing, and changing.

## Features
- **User System:** Unique username registration and secure login.
- **Product Catalog:** Persistent storage of products with ID, name, price, and stock levels.
- **Shopping Cart:** Add, remove, or reduce item quantities. Carts are unique to each user and persist across sessions.
- **Checkout System:** Performs final stock validation before deducting quantities and generating receipts.
- **Order History:** Users can view their past purchases at any time.

## Bonus Features Implemented
1. **Password Hashing:** Uses the `hashlib` library to store hashes of passwords rather than plain text for security.
2. **Receipt Export:** On successful checkout, a formatted receipt is automatically exported as a `.txt` file.

## Data Storage
The system uses JSON files for data persistence:
- `users.json`: Authenticated user accounts.
- `products.json`: Current store inventory.
- `carts.json`: Saved shopping carts mapped to usernames.
- `orders.json`: Permanent history of all successful transactions.

## How to Run
1. Ensure Python is installed on your system.
2. Place all `.py` and `.json` files in the same directory.
3. Launch the program by running main.py.
