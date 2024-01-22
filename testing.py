import json
import os

OPENING_MOVES_JSON_RELATIVE_PATH = "move_archive/openings.json"

filepath = os.getcwd() + "/" + OPENING_MOVES_JSON_RELATIVE_PATH

try:
    with open(filepath, 'r') as file:
        opening_moves_prep = json.load(file)
    print("Opening moves loaded successfully.")
except FileNotFoundError:
    print(f"File not found: {filepath}")
except json.JSONDecodeError:
    print(f"Error decoding JSON from file: {filepath}")
except Exception as e:
    print(f"An error occurred while loading the file: {e}")
    
key = "1014315135151802913"
    
print(key in opening_moves_prep["BLACK"])
print(opening_moves_prep["BLACK"][key])