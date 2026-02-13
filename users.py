import storage
import hashlib

#hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_or_login():
    
    newORexistingUser = input("Press 1 to Register, 2 to Login: ")

    if newORexistingUser == "1":
        username = input("Enter your desired username: ")
        users = storage.read_file('users.json')
        is_taken = False

        for user in users:
            if user.get("account", {}).get("username") == username:
                is_taken = True
                break
                
        while is_taken:
            #if username is already taken, prompts user to enter a different username
            print("Username already exists please choose a different one.")
            username = input("Enter your desired username: ")
            is_taken = False

            #checks if username is already taken
            for user in users:
                if user.get("account", {}).get("username") == username:
                    is_taken = True
                    break
        else:
            password = input("Enter your desired password: ")
            # ensures password is at least 6 characters long
            while len(password) < 6:
                print("Password must be at least 6 characters long.")
                password = input("Enter your desired password: ")
            else:
                data_to_store = {
                    "account": {
                        "username": username,
                        "password": hash_password(password) #store hashed password instead of plain text
                    }
                }
                storage.append_to_file(data_to_store, 'users.json')
                print("Registration successful!")
                return username
            
#login function
    elif newORexistingUser == "2":
        while True:
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            
            #reads users from file and checks if username and hashed password match any existing user
            users = storage.read_file('users.json')
            login_successful = False
            hashed_input = hash_password(password)
            for user in users:
                if (user.get("account", {}).get("username") == username and
                    user.get("account", {}).get("password") == hashed_input):
                    login_successful = True
                    break
                
            if login_successful:
                print("Login successful!")
                return username
            else:
                print("Invalid username or password.")
                