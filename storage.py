import json
from pprint import pprint
import os

def save_to_file(data, filename):
    #Saves the data to a file in JSON format.
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def read_file(filename):
    #Loads data from a JSON file. Creates the file if it doesn't exist.
    if not os.path.exists(filename):
        save_to_file([], filename)
        return []

    #Reads the file
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        save_to_file([], filename)
        return []
    
def append_to_file(data, filename):
    #changes data to a JSON file.
    try:
        existing_data = read_file(filename)
    except FileNotFoundError:
        existing_data = []
    
    if not isinstance(existing_data, list):
        raise ValueError("Existing data is not a list; cannot append.")
    
    existing_data.append(data)
    
    save_to_file(existing_data, filename)

def clean_file(filename):
    save_to_file([], filename)