
import csv
import datetime
from hashmap import HashTable
from package import Package
from truck import Truck

# Load distance and address data from CSV files for calculating distances between addresses
with open("csv/distances.csv") as f:
    distance_data = list(csv.reader(f))

with open("csv/addresses.csv") as f:
    address_data = list(csv.reader(f))


# Function: load_packages
# Purpose: This function loads package data from a CSV file into a custom HashTable.
# The 'filename' argument is the CSV file containing package details like address, deadline, and delivery status.
# Each row in the CSV represents a Package object, which is then inserted into the HashTable.
# Why: Storing packages in a HashTable allows for fast lookups during the delivery process.
# How: The CSV reader parses each row, creates a Package object, and inserts it into the hash table using the package ID as the key.
def load_packages(filename):
    packages = HashTable() # Initialize the hash table
    with open(filename) as file:
        reader = csv.reader(file)
        # Read each row of the CSV file and create Package objects
        for row in reader:
            package_id = int(row[0])
            package = Package(package_id, row[1], row[2], row[3], row[4], row[5], row[6], "At Hub")
            packages.insert(package_id, package) # Insert the package into the hash table
    return packages # Return the filled hash table

# Calculate the distance between two addresses.
# The 'from_address' and 'to_address' arguments are looked up in the address_data list,
# and the corresponding distance is retrieved from the distance_data CSV.
def get_distance(from_address, to_address):
    hub_address = "4001 South 700 East"

    # Function to find the index of a given address in the address data.
    def find_address_index(address):
        if address == "410 S. State St.": # Handle a special case for address lookup
            return next(int(row[0]) for row in address_data if "410 S State St" in row[2])
        try:
            # Search for the address in the list of addresses
            return next(int(row[0]) for row in address_data if address in row[2])
        except StopIteration:
            # If the address is not found, use the hub address as a fallback
            print(f"Warning: Address '{address}' not found in data. Using hub address instead.")
            return next(int(row[0]) for row in address_data if hub_address in row[2])

    # Get indices of the from and to addresses
    from_idx = find_address_index(from_address)
    to_idx = find_address_index(to_address)

    # Retrieve the distance between the two addresses
    distance = distance_data[from_idx][to_idx] or distance_data[to_idx][from_idx]
    return float(distance)


# Function: nearest_neighbor
# Purpose: This function optimizes the delivery route for a truck using the Nearest Neighbor algorithm.
# The goal is to minimize the total distance traveled by always selecting the closest package's destination
# from the truck's current location.
# Why: Nearest Neighbor is a simple but effective heuristic to reduce total mileage in routing problems like
# package delivery.
# How:
# 1. The truck's current location is set to its departure point.
# 2. The function iterates through the undelivered packages on the truck.
# 3. For each iteration, it calculates the distance between the current location and the destination of each package.
# 4. The nearest package is selected for delivery, and the truck's location is updated.
# 5. This process continues until all packages on the truck are delivered.
def nearest_neighbor(truck, packages, distance_data):
    # Implement the Nearest Neighbor algorithm for package delivery
    current_address = truck.current_location
    # Find the nearest undelivered package by checking the distance to each package.
    while truck.package_ids:  # Changed from packages to package_ids
        try:
            next_package = min(truck.package_ids, key=lambda p: get_distance(current_address, packages.lookup(p).get_current_address(truck.current_time)))
        except Exception as e:
            print(f"Error finding next package: {e}")
            if truck.package_ids:
                next_package = truck.package_ids[0]
            else:
                break

        package = packages.lookup(next_package)

        try:
            # Calculate the distance to the package address and estimate the delivery time.
            distance = get_distance(current_address, package.get_current_address(truck.current_time))
            delivery_time = datetime.timedelta(hours=distance / truck.speed)

            # Update the package's departure and delivery times.
            package.departure_time = truck.depart_time
            package.delivery_time = truck.current_time + delivery_time

            # Deliver the package, updating the truck's current status.
            truck.deliver_package(next_package, distance, delivery_time)
            current_address = package.get_current_address(truck.current_time)
        except Exception as e:
            print(f"Error delivering package {next_package}: {e}")
            truck.package_ids.remove(next_package)  # Changed from packages to package_ids


# Utility function to format time for display
def format_time(time_delta):
    # Convert timedelta to formatted string (HH:MM:SS)
    hours, remainder = divmod(time_delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def get_truck_number(package, trucks):
    for truck in trucks:
        if truck.has_package(package.id):
            return truck.id
    return "N/A"

# Function: show_package_status
# Purpose: This function displays the current status of all packages at a given time.
# Why: The user may want to check the status of packages at a specific point in time (e.g., whether they are still at the hub, en route, or delivered).
# How:
# 1. The function accepts a hash table containing all package data and a 'check_time' for status.
# 2. It iterates through all packages in the hash table, updating their status based on their delivery and departure times.
# 3. For each package, it prints the ID, address, status (at hub, en route, delivered), and other package details.
def show_package_status(package_hash, check_time, trucks):
    # Display status of all packages at a given time
    print(f"\nPackage Status at {format_time(check_time)}:")
    print("-" * 140)
    print(f"{'ID':^4} | {'Address':^30} | {'City':^15} | {'State':^5} | {'Zip':^5} | {'Deadline':^10} | {'Weight':^8} | {'Status':^10} | {'Truck':^5} | {'Delivery Time':^15}")
    print("-" * 140)
    for i in range(1, 41):
        package = package_hash.lookup(i)
        if package:
            package.check_and_update_address(check_time)  # Add this line to update the address
            package.update_status(check_time)
            truck_num = get_truck_number(package, trucks)
            delivery_time = format_time(package.delivery_time) if package.delivery_time else "N/A"
            print(f"{package.id:^4} | {package.address:<30} | {package.city:<15} | {package.state:^5} | {package.zipcode:^5} | {package.deadline:^10} | {package.weight:^8} | {package.status:^10} | {truck_num:^5} | {delivery_time:^15}")

# Display the status of all packages on a specific truck within a given time frame.
# Iterates through the packages on the truck and checks if they were delivered within the time range.
def show_truck_packages_status_for_timeframe(truck, package_hash, start_time, end_time):
    print(
        f"\nPackages status for truck {truck.id} departing at {format_time(truck.depart_time)} between {format_time(start_time)} and {format_time(end_time)}:")
    print("-" * 70)
    print(f"{'Package ID':^10} | {'Status':^15} | {'Delivery Time':^15} | {'Address':^25}")
    print("-" * 70)
    # Iterate through the packages on the truck and display their status.
    for package_id in truck.all_package_ids:
        package = package_hash.lookup(package_id)
        if package.delivery_time <= end_time:
            if package.delivery_time <= start_time:
                status = "Delivered"
                delivery_time = format_time(package.delivery_time)
            elif start_time < package.delivery_time <= end_time:
                status = "Delivered"
                delivery_time = format_time(package.delivery_time)
            else:
                status = "En route"
                delivery_time = "N/A"

            package.check_and_update_address(end_time)
            print(f"{package_id:^10} | {status:^15} | {delivery_time:^15} | {package.address:<25}")

# Calculate and display total mileage traveled by all trucks
# Displays individual truck mileage and the total mileage for all trucks combined.
def show_total_mileage(trucks):
    print("\nMileage Report:")
    for truck in trucks:
        print(f"Truck {truck.id}: {truck.mileage:.2f} miles")
    total_mileage = sum(truck.mileage for truck in trucks)
    print(f"\nTotal mileage for all trucks: {total_mileage:.2f} miles")

# Initialize the trucks with their assigned package lists and departure times.
# Returns the initialized truck objects.
def initialize_trucks(package_hash):
    truck1_packages = [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40]
    truck2_packages = [3, 18, 36, 38]
    truck3_packages = [2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 17, 19, 21, 22, 23, 24, 25, 26, 27, 28, 32, 33, 35, 39]

    # Create truck objects with departure times and package lists
    truck1 = Truck(1, 16, 18, truck1_packages, "4001 South 700 East", depart_time=datetime.timedelta(hours=8))
    truck2 = Truck(2, 16, 18, truck2_packages, "4001 South 700 East", depart_time=datetime.timedelta(hours=9, minutes=5))
    truck3 = Truck(3, 16, 18, truck3_packages, "4001 South 700 East", depart_time=datetime.timedelta(hours=10, minutes=20))

    return truck1, truck2, truck3

# Simulate the delivery process for all trucks using the Nearest Neighbor algorithm.
# Trucks will deliver their assigned packages by optimizing their delivery route.
def run_delivery_simulation(truck1, truck2, truck3, package_hash):
    nearest_neighbor(truck1, package_hash, distance_data)
    nearest_neighbor(truck2, package_hash, distance_data)
    nearest_neighbor(truck3, package_hash, distance_data)

# Main program function: Provides the user interface and allows the user to interact with the system.
# The user can check package status, view total mileage, or exit the program.
def main():
    print("Welcome to WGUPS Package Tracking System")

    # Load package data and initialize the trucks
    package_hash = load_packages("csv/packages.csv")
    truck1, truck2, truck3 = initialize_trucks(package_hash)
    run_delivery_simulation(truck1, truck2, truck3, package_hash)

    trucks = [truck1, truck2, truck3]

    # Main program loop
    while True:
        print("\nMenu Options:")
        print("1. View status of all packages at a specific time")
        print("2. View status of a specific package")
        print("3. View package status for specific time frame")
        print("4. View total mileage (all trucks and individual)")
        print("5. Exit")

        # Get user input for menu choice
        choice = input("Enter your choice (1-5): ")

        # Process user's choice
        if choice == '1':
            # Option 1: Check status of all packages at a specific time
            time_input = input("Enter time to check status (HH:MM): ")
            try:
                h, m = map(int, time_input.split(":"))
                check_time = datetime.timedelta(hours=h, minutes=m)
                show_package_status(package_hash, check_time, trucks)
            except ValueError:
                print("Invalid time format. Please use HH:MM.")

        elif choice == '2':
            # Option 2: Check status of a specific package at a specific time
            package_id = input("Enter package ID: ")
            time_input = input("Enter time to check status (HH:MM): ")
            try:
                package_id = int(package_id)
                h, m = map(int, time_input.split(":"))
                check_time = datetime.timedelta(hours=h, minutes=m)
                package = package_hash.lookup(package_id)
                if package:
                    package.check_and_update_address(check_time)
                    package.update_status(check_time)
                    truck_num = get_truck_number(package, trucks)
                    delivery_time = format_time(package.delivery_time) if package.delivery_time else "N/A"
                    print("\nPackage Details:")
                    print("-" * 70)
                    print(f"Package ID: {package.id}")
                    print(f"Address: {package.address}")
                    print(f"City: {package.city}")
                    print(f"State: {package.state}")
                    print(f"Zip: {package.zipcode}")
                    print(f"Deadline: {package.deadline}")
                    print(f"Weight: {package.weight}")
                    print(f"Status: {package.status}")
                    print(f"Truck: {truck_num}")
                    print(f"Delivery Time: {delivery_time}")
                else:
                    print("Package not found.")
            except ValueError:
                print("Invalid input. Please enter a valid package ID and time (HH:MM).")

        elif choice == '3':
            # Option 3: View package status for a specific time frame
            print("\nSelect a time frame:")
            print("1. 8:35 a.m. to 9:25 a.m.")
            print("2. 9:35 a.m. to 10:25 a.m.")
            print("3. 12:03 p.m. to 1:12 p.m.")
            time_choice = input("Enter your choice (1-3): ")

            # Set start and end times based on user's selection
            if time_choice == '1':
                start_time = datetime.timedelta(hours=8, minutes=35)
                end_time = datetime.timedelta(hours=9, minutes=25)
            elif time_choice == '2':
                start_time = datetime.timedelta(hours=9, minutes=35)
                end_time = datetime.timedelta(hours=10, minutes=25)
            elif time_choice == '3':
                start_time = datetime.timedelta(hours=12, minutes=3)
                end_time = datetime.timedelta(hours=13, minutes=12)
            else:
                print("Invalid choice. Please select 1, 2, or 3.")
                continue

            # Display the status of packages within the selected time frame for each truck
            for truck in trucks:
                show_truck_packages_status_for_timeframe(truck, package_hash, start_time, end_time)

        elif choice == '4':
            # Option 4: View the total mileage for all trucks
            show_total_mileage(trucks)

        elif choice == '5':
            # Option 5: Exit the program
            print("Thank you for using WGUPS Package Tracking System. Goodbye!")
            break

        else:
            # Handle invalid menu choices
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()