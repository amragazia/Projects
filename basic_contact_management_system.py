import re
import json
import sys

# --- Regular Expressions ---
NAME_RE = re.compile(r"^[A-Za-z]+([ '-][A-Za-z]+)*$")
AGE_RE = re.compile(r"^[0-9]{1,3}$")
PHONE_NUMBER_RE = re.compile(r"^(010|011|012|015)\d{8}$")
EMAIL_RE = re.compile(r"^[\w.]+@[A-Za-z]+\.[A-Za-z]{2,}$")
ADDRESS_RE = re.compile(r"^[A-Za-z0-9\s,.-]+$")  # District, City, Country(EGYPT) 
INPUT_1OR2_RE = re.compile(r"^[12]$")
MENU_CHOICE_RE = re.compile(r"^[1-6]$")

# --- Global Data ---
contacts = []

# A dictionary to hold all validation rules for easy access.
VALIDATION_RULES = {
    "Name": NAME_RE,
    "Age": AGE_RE,
    "Phone Number": PHONE_NUMBER_RE,
    "Email": EMAIL_RE,
    "Address": ADDRESS_RE,
    "Delete Choice": INPUT_1OR2_RE,
    "Menu": MENU_CHOICE_RE
}


# --- Core Functions ---
def load_data():
    # Loads contacts from a JSON file, returning an empty list on failure.
    try:
        with open("contacts.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data():
    # Saves the entire contacts list to the JSON file.
    with open("contacts.json", "w") as f:
        json.dump(contacts, f, indent=4)

def validate_entry(prompt, validation_key):
    # A streamlined function to get and validate user input using the rules dictionary.
    regex = VALIDATION_RULES[validation_key]
    while True:
        user_input = input(f"{prompt}: ").strip()
        if regex.fullmatch(user_input):
            return user_input
        else:
            print("Invalid entry, please try again. ❌")


# --- Feature Functions ---
def add_contact():
    # Adds a new contact to the list.
    print("\n--- ➕ Add a New Contact ---")
    contact = {
        "Name" : validate_entry("Enter Name", "Name"),
        "Age" : validate_entry("Enter Age", "Age"),
        "Phone Number" : validate_entry("Enter Phone Number", "Phone Number"),
        "Email" : validate_entry("Enter Email", "Email"),
        "Address" : validate_entry("Enter Address", "Address")
        }
    contacts.append(contact)
    save_data()
    print("Contact added successfully! ✅")

def delete_contact():
    # Deletes a contact by their phone number.
    global contacts
    print("\n--- 🗑️ Delete a Contact ---")
    phone_to_delete = validate_entry("Enter the Phone Number of the contact to delete", "Phone Number")
    
    original_count = len(contacts)
    # Use a list comprehension for safe and efficient removal.
    contacts = [c for c in contacts if c["Phone Number"] != phone_to_delete]
    if len(contacts) < original_count:
        print("Contact deleted successfully! ✅")
        save_data()
    else:
        print("No contact found with that phone number. 🤷")
            
def search_contact():
    # Searches for contacts by name and displays them.
    print("\n--- 🔍 Search for a Contact ---")
    # Use a list comprehension to find all matching contacts
    name_to_find = validate_entry("Enter Name to search for", "Name")
    results = [c for c in contacts if c["Name"].lower() == name_to_find.lower()]

    if not results:
        print("No results found. 🤷")
        return
    print(f"Found {len(results)} contact(s):")
    for contact in results:
        print("-" * 20)
        for key, val in contact.items():
            print(f"{key}: {val}")
    print("-" * 20)

def update_contact():
    print("\n--- 🔄 Update a Contact ---")
    phone_to_find = validate_entry("Enter Phone Number of the contact to update", "Phone Number")

    for index, c in enumerate(contacts):
        if c["Phone Number"] == phone_to_find:
            print("\nFound Contact:")
            for key, val in c.items():
                print(f"{key}: {val}")
            print("-" * 20)

            print("\n--- Enter New Contact Details ---")
            for key in c.keys():
                c[key] = validate_entry(f"Enter {key}", key)

            contacts[index] = c
            save_data()
            print("Contact updated successfully! ✅")
            return

    print("No contact found with that phone number. 🤷")

    


def get_all_contacts():
    # Displays all saved contacts.
    print("\n--- 📖 All Contacts ---")
    if not contacts:
        print("Your contact list is empty.")
        return
    
    for i, contact in enumerate(contacts, 1):
        print(f"--- Contact {i} ---")
        for key, val in contact.items():
            print(f"{key}: {val}")

    print("\n" + "=" * 20)

def exit_program():
    # Exits the program.
    print("\nGoodbye! 👋")
    sys.exit()



def main_menu():
    # Displays the main menu options.
    print("\n" + "="*5 + " 📞 Contact Manager " + "="*5)
    print("1. Add contact")
    print("2. Delete contact")
    print("3. Search contact")
    print("4. Update contact")
    print("5. Show all contacts")
    print("6. Exit")
    print("=" * 30)


# --- Main Execution ---
if __name__ == "__main__":
    contacts = load_data()

    # A dictionary mapping menu choices to functions
    function_map = {
        "1" : add_contact,
        "2" : delete_contact,
        "3" : search_contact,
        "4" : update_contact,
        "5" : get_all_contacts,
        "6" : exit_program
    }

    while True:
        main_menu()
        choice = validate_entry("Choose an option", "Menu")

        # Get the function from the dictionary and call it
        action = function_map[choice]
        action()