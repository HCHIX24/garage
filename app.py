import json
import os
from enum import Enum

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
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return print ["FILE NOT FOUND"]

# Function to save data back to JSON files
def save_data(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# Function to clear the console screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to add a new car to the list and save it
def add_car(cars):
    car_id = input("Enter Car ID: ")
    for car in cars:
        if car['Id'] == car_id:
            print("This ID already exists!")
            return
    color = input("Enter Car Color: ")
    brand = input("Enter Car Brand: ")
    owner_id = input("Enter Owner ID: ")
    cars.append({'Id': car_id, 'Color': color, 'Brand': brand, 'OwnerId': owner_id})
    save_data(car_filename, cars)
    print(f"{color} {brand} has been added.")

# Function to delete a car from the list based on ID
def delete_car(cars):
    car_id = input("Enter Car ID to delete: ")
    for i, car in enumerate(cars):
        if car['Id'] == car_id:
            del cars[i]
            save_data(car_filename, cars)
            print(f"{car['Color']} {car['Brand']} has been deleted.")
            return
    print("Car ID not found.")

# Function to edit the details of an existing car
def edit_car(cars):
    car_id = input("Enter Car ID to edit: ")
    for car in cars:
        if car['Id'] == car_id:
            print(f"Current Data: {car}")
            car['Color'] = input("Enter new Car Color: ")
            car['Brand'] = input("Enter new Car Brand: ")
            car['OwnerId'] = input("Enter new Owner ID: ")
            save_data(car_filename, cars)
            print(f"Car ID {car_id} has been updated.")
            return
    print("Car ID not found.")

# Function to display all cars in the list
def show_all_cars(cars):
    if not cars:
        print("No cars available.")
    else:
        for car in cars:
            print(f"ID-{car['Id']}: {car['Color']} {car['Brand']} (Owner ID: {car['OwnerId']})")

# Function to search for a car based on ID, color, or brand
def search_car(cars):
    search_by = input("Search by (id/color/brand/ownerid): ").lower()
    search_term = input("Enter search term: ").lower()
    found = False
    for car in cars:
        if car[search_by].lower() == search_term:
            print(f"Found: {car}")
            found = True
    if not found:
        print("No matching car found.")

# Function to add a new customer to the list and save it
def add_customer(customers):
    customer_id = input("Enter Customer ID: ")
    for customer in customers:
        if customer['Id'] == customer_id:
            print("This ID already exists!")
            return
    name = input("Enter Customer Name: ")
    email = input("Enter Customer Email: ")
    customers.append({'Id': customer_id, 'Name': name, 'Email': email})
    save_data(customer_filename, customers)
    print(f"{name} has been added.")

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
        print("Pink and Cute Garage")
        print("====================")
        for option in MenuOptions:
            print(f"{option.value} - {option.name.replace('_', ' ').title()}")
        choice = input("Select an option: ")

        if choice.isdigit() and MenuOptions(int(choice)) in MenuOptions:
            option = MenuOptions(int(choice))
            if option == MenuOptions.ADD_CAR:
                add_car(cars)
            elif option == MenuOptions.DELETE_CAR:
                delete_car(cars)
            elif option == MenuOptions.EDIT_CAR:
                edit_car(cars)
            elif option == MenuOptions.SHOW_ALL_CARS:
                show_all_cars(cars)
                input("Press Enter to continue...")  # Wait for user input before clearing the screen
            elif option == MenuOptions.SEARCH_CAR:
                search_car(cars)
                input("Press Enter to continue...")  # Wait for user input before clearing the screen
            elif option == MenuOptions.ADD_CUSTOMER:
                add_customer(customers)
            elif option == MenuOptions.SHOW_ALL_CUSTOMERS:
                show_all_customers(customers)
                input("Press Enter to continue...")  # Wait for user input before clearing the screen
            elif option == MenuOptions.CLEAR:
                clear_screen()
            elif option == MenuOptions.EXIT:
                save_data(car_filename, cars)
                save_data(customer_filename, customers)
                print("Goodbye!")
                break
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")  # Wait for user input before clearing the screen

if __name__ == "__main__":
    main()

