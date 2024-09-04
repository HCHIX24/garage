from enum import Enum
import os, json

# File names for the JSON data
car_filename = 'p_garage.json'
customer_filename = 'customers.json'

# Enum to represent menu options for the CRUD operations
class MenuOptions(Enum):
    ADD_CAR = 1
    DELETE_CAR = 2
    EDIT_CAR = 3
    SHOW_ALL_CARS = 4
    SEARCH_CAR = 5
    ADD_CUSTOMER = 6
    SHOW_ALL_CUSTOMERS = 7
    CLEAR = 8
    EXIT = 9

# Function to load data from JSON files
def load_data(filename):
    if not os.path.exists(filename):
        return []  # Return an empty list if the file does not exist
    with open(filename, 'r') as file:
        return json.load(file)

# Function to save data back to JSON files
def save_data(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# Function to clear the console screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to find a customer by ID
def find_customer(customers, customer_id):
    for customer in customers:
        if customer['Id'] == customer_id:
            return customer
    return None

# Function to add or update a car with customer handling
def add_car(cars, customers):
    car_id = input("Enter Car ID: ")
    if any(car['Id'] == car_id for car in cars):
        print("This Car ID already exists!")
        return

    color = input("Enter Car Color: ")
    brand = input("Enter Car Brand: ")
    owner_id = input("Enter Owner ID (Press Enter if new customer needed): ")
    
    if owner_id:
        # Check if the customer exists
        customer = find_customer(customers, owner_id)
        if not customer:
            print("Customer not found. Please add the customer first.")
            return
        # Add car to existing customer
        cars.append({'Id': car_id, 'Color': color, 'Brand': brand, 'OwnerIds': [owner_id]})
    else:
        # Add car without an owner and prompt for new customer details
        print("Adding car without an owner. Please add a customer now.")
        add_customer(customers, car_id, color, brand)

    save_data(car_filename, cars)
    print(f"{color} {brand} has been added.")

# Function to add or update a customer with car handling
def add_customer(customers, car_id=None, car_color=None, car_brand=None):
    customer_id = input("Enter Customer ID: ")
    if any(customer['Id'] == customer_id for customer in customers):
        print("This Customer ID already exists!")
        return

    name = input("Enter Customer Name: ")
    email = input("Enter Customer Email: ")
    customer = {'Id': customer_id, 'Name': name, 'Email': email}
    customers.append(customer)

    # Add car if provided
    if car_id:
        cars = load_data(car_filename)
        cars.append({'Id': car_id, 'Color': car_color, 'Brand': car_brand, 'OwnerIds': [customer_id]})
        save_data(car_filename, cars)

    save_data(customer_filename, customers)
    print(f"{name} has been added.")

# Function to delete a car from the list based on ID
def delete_car(cars):
    car_id = input("Enter Car ID to delete: ")
    for i, car in enumerate(cars):
        if car['Id'] == car_id:
            del cars[i]
            save_data(car_filename, cars)
            print(f"Car ID-{car_id} has been deleted.")
            return
    print("Car ID not found.")

# Function to edit the details of an existing car
def edit_car(cars, customers):
    car_id = input("Enter Car ID to edit: ")
    for car in cars:
        if car['Id'] == car_id:
            print(f"Current Data: {car}")
            car['Color'] = input("Enter new Car Color: ")
            car['Brand'] = input("Enter new Car Brand: ")
            owner_ids_input = input("Enter new Owner IDs (comma-separated): ")
            owner_ids = [owner_id.strip() for owner_id in owner_ids_input.split(',')]
            
            # Validate owner IDs
            valid_owner_ids = all(owner_id in [customer['Id'] for customer in customers] for owner_id in owner_ids)
            if not valid_owner_ids:
                print("One or more Owner IDs are invalid!")
                return
            
            car['OwnerIds'] = owner_ids
            save_data(car_filename, cars)
            print(f"Car ID {car_id} has been updated.")
            return
    print("Car ID not found.")

# Function to display all cars in the list
def show_all_cars(cars, customers):
    if not cars:
        print("No cars available.")
    else:
        for car in cars:
            owners = ', '.join(customer['Name'] for customer in customers if customer['Id'] in car['OwnerIds'])
            print(f"ID-{car['Id']}: {car['Color']} {car['Brand']} (Owners: {owners})")

# Function to search for a car based on ID, color, or brand
def search_car(cars, customers):
    search_by = input("Search by (id/color/brand/ownerid): ").lower()
    search_term = input("Enter search term: ").lower()
    found = False
    for car in cars:
        if search_by == 'ownerid':
            if any(owner_id.lower() == search_term for owner_id in car['OwnerIds']):
                print(f"Found: {car}")
                found = True
        elif car.get(search_by, '').lower() == search_term:
            print(f"Found: {car}")
            found = True
    if not found:
        print("No matching car found.")

# Function to display all customers in the list
def show_all_customers(customers):
    if not customers:
        print("No customers available.")
    else:
        for customer in customers:
            print(f"ID-{customer['Id']}: {customer['Name']} (Email: {customer['Email']})")

# Main function to handle the user interface and call the relevant functions
def main():
    cars = load_data(car_filename)
    customers = load_data(customer_filename)
    while True:
        clear_screen()
        print("Pink Garage")
        print("====================")
        for option in MenuOptions:
            print(f"{option.value} - {option.name.replace('_', ' ').title()}")
        choice = input("Select an option: ")

        if choice.isdigit() and MenuOptions(int(choice)) in MenuOptions:
            option = MenuOptions(int(choice))
            if option == MenuOptions.ADD_CAR:
                add_car(cars, customers)
            elif option == MenuOptions.DELETE_CAR:
                delete_car(cars)
            elif option == MenuOptions.EDIT_CAR:
                edit_car(cars, customers)
            elif option == MenuOptions.SHOW_ALL_CARS:
                show_all_cars(cars, customers)
                input("Press Enter to continue...")
            elif option == MenuOptions.SEARCH_CAR:
                search_car(cars, customers)
                input("Press Enter to continue...")
            elif option == MenuOptions.ADD_CUSTOMER:
                add_customer(customers)
            elif option == MenuOptions.SHOW_ALL_CUSTOMERS:
                show_all_customers(customers)
                input("Press Enter to continue...")
            elif option == MenuOptions.CLEAR:
                clear_screen()
            elif option == MenuOptions.EXIT:
                save_data(car_filename, cars)
                save_data(customer_filename, customers)
                print("Goodbye!")
                break
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()

