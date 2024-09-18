# Logan Arguello
# Student ID# 012053764
# C950

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


# Load package data from a CSV file into a hash table.
# Each package is represented by a Package object, and this function populates a HashTable with package information.
# The 'filename' argument specifies the CSV file containing package details.
def load_packages(filename):
    # Load package data from CSV file into a hash table
    packages = HashTable()
    with open(filename) as file:
        reader = csv.reader(file)
        for row in reader:
            package_id = int(row[0])
            # Create a Package object and insert it into the hash table
            package = Package(package_id, row[1], row[2], row[3], row[4], row[5], row[6], "At Hub")
            packages.insert(package_id, package)
    return packages


# Calculate the distance between two addresses.
# The 'from_address' and 'to_address' arguments are looked up in the address_data list,
# and the corresponding distance is retrieved from the distance_data CSV.
def get_distance(from_address, to_address):
    # Calculate distance between two addresses using the distance data
    from_idx = next(int(row[0]) for row in address_data if from_address in row)
    to_idx = next(int(row[0]) for row in address_data if to_address in row)
    distance = distance_data[from_idx][to_idx] or distance_data[to_idx][from_idx]
    return float(distance)


# This function implements the Nearest Neighbor algorithm to optimize package delivery routing for a truck.
# It selects the nearest package to the truck's current location, delivers it, and repeats the process until all packages are delivered.
def nearest_neighbor(truck, packages, distance_data):
    # Implement the Nearest Neighbor algorithm for package delivery
    current_address = truck.current_location
    while truck.packages:
        # Find the nearest undelivered package by checking the distance to each package.
        next_package = min(truck.packages, key=lambda p: get_distance(current_address, packages.lookup(p).address))
        package = packages.lookup(next_package)

        # Calculate the distance to the package address and estimate the delivery time.
        distance = get_distance(current_address, package.address)
        delivery_time = datetime.timedelta(hours=distance / truck.speed)

        # Update the package's departure and delivery times.
        package.departure_time = truck.depart_time
        package.delivery_time = truck.current_time + delivery_time

        # Deliver the package, updating the truck's current status.
        truck.deliver_package(next_package, distance, delivery_time)
        current_address = package.address

# This is used to display times in a readable format.
def format_time(time_delta):
    # Convert timedelta to formatted string (HH:MM:SS)
    hours, remainder = divmod(time_delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def show_package_status(package_hash, check_time):
    # Display status of all packages at a given time
    print(f"\nPackage Status at {format_time(check_time)}:")
    print("-" * 120)
    print(f"{'ID':^4} | {'Address':^30} | {'City':^15} | {'State':^5} | {'Zip':^5} | {'Deadline':^10} | {'Weight':^8} | {'Status':^10}")
    print("-" * 120)
    for i in range(1, 41):
        package = package_hash.lookup(i)
        if package:
            package.update_status(check_time)
            print(f"{package.id:^4} | {package.address:<30} | {package.city:<15} | {package.state:^5} | {package.zipcode:^5} | {package.deadline:^10} | {package.weight:^8} | {package.status:^10}")



def show_truck_packages_status(truck, package_hash, start_time, end_time):
    print(f"\nPackages status for truck departing at {format_time(truck.depart_time)} between {format_time(start_time)} and {format_time(end_time)}:")
    print("-" * 50)
    print(f"{'Package ID':^10} | {'Status':^15} | {'Delivery Time':^15}")
    print("-" * 50)
    # Iterate through the packages on the truck and display their status.
    for package_id in truck.all_packages:
        package = package_hash.lookup(package_id)
        if package.delivery_time and package.delivery_time <= end_time:
            status = "Delivered"
            delivery_time = format_time(package.delivery_time)
        elif package.departure_time and start_time <= package.departure_time <= end_time:
            status = "En route"
            delivery_time = "N/A"
        elif package.departure_time and package.departure_time < start_time:
            status = "En route"
            delivery_time = "N/A"
        else:
            status = "At hub"
            delivery_time = "N/A"
        print(f"{package_id:^10} | {status:^15} | {delivery_time:^15}")


def show_total_mileage(trucks):
    # Calculate and display total mileage traveled by all trucks
    total_mileage = sum(truck.mileage for truck in trucks)
    print(f"Total mileage traveled by all trucks: {total_mileage:.2f}")

# Display the status of packages for a specific truck within a given time frame.
# It shows whether the packages were delivered, en route, or still at the hub during the selected time window.
def show_truck_packages_status_for_timeframe(truck, package_hash, start_time, end_time):
    print(f"\nPackages status for truck departing at {format_time(truck.depart_time)} between {format_time(start_time)} and {format_time(end_time)}:")
    print("-" * 50)
    print(f"{'Package ID':^10} | {'Status':^15} | {'Delivery Time':^15}")
    print("-" * 50)
    for package_id in truck.all_packages:
        package = package_hash.lookup(package_id)
        if start_time <= package.delivery_time <= end_time:
            status = "Delivered"
            delivery_time = format_time(package.delivery_time)
        elif package.departure_time <= end_time and (package.delivery_time is None or package.delivery_time > end_time):
            status = "En route"
            delivery_time = "N/A"
        else:
            continue  # Skip packages not relevant to this time frame
        print(f"{package_id:^10} | {status:^15} | {delivery_time:^15}")


def main():
    # Main function to run the WGUPS Package Tracking System
    print("Welcome to WGUPS Package Tracking System")

    while True:
        # Display menu options
        print("\nMenu Options:")
        print("1. Check status of all packages")
        print("2. Check status of a specific package")
        print("3. View total mileage")
        print("4. View package status for specific time frame")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            # Check status of all packages at a specific time
            time_input = input("Enter time to check status (HH:MM): ")
            try:
                h, m = map(int, time_input.split(":"))
                check_time = datetime.timedelta(hours=h, minutes=m)
                show_package_status(package_hash, check_time)
            except ValueError:
                print("Invalid time format. Please use HH:MM.")

        elif choice == '2':
            # Check status of a specific package at a specific time
            package_id = input("Enter package ID: ")
            time_input = input("Enter time to check status (HH:MM): ")
            try:
                package_id = int(package_id)
                h, m = map(int, time_input.split(":"))
                check_time = datetime.timedelta(hours=h, minutes=m)
                package = package_hash.lookup(package_id)
                if package:
                    package.update_status(check_time)
                    print("\nPackage Details:")
                    print("-" * 50)
                    print(f"Package ID: {package.id}")
                    print(f"Address: {package.address}")
                    print(f"City: {package.city}")
                    print(f"State: {package.state}")
                    print(f"Zip: {package.zipcode}")
                    print(f"Deadline: {package.deadline}")
                    print(f"Weight: {package.weight}")
                    print(f"Status: {package.status}")
                    if package.delivery_time:
                        print(f"Delivery Time: {format_time(package.delivery_time)}")
                else:
                    print("Package not found.")
            except ValueError:
                print("Invalid input. Please enter a valid package ID and time (HH:MM).")

        elif choice == '3':
            # View total mileage for all trucks
            show_total_mileage([truck1, truck2, truck3])

        elif choice == '4':
            # View package status for a specific time frame
            print("\nSelect a time frame:")
            print("1. 8:35 a.m. to 9:25 a.m.")
            print("2. 9:35 a.m. to 10:25 a.m.")
            print("3. 12:03 p.m. to 1:12 p.m.")
            time_choice = input("Enter your choice (1-3): ")

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
            for truck in [truck1, truck2, truck3]:
                show_truck_packages_status_for_timeframe(truck, package_hash, start_time, end_time)

        elif choice == '5':
            # Exit the program
            print("Thank you for using WGUPS Package Tracking System. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    # Load packages and initialize trucks
    package_hash = load_packages("csv/packages.csv")

    # Assign packages to trucks (manually based on constraints)
    truck1_packages = [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40]
    truck2_packages = [3, 18, 36, 38]
    truck3_packages = [2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 17, 19, 21, 22, 23, 24, 25, 26, 27, 28, 32, 33, 35, 39]

    # Create truck objects with packages and departure times
    truck1 = Truck(16, 18, truck1_packages, "4001 South 700 East", depart_time=datetime.timedelta(hours=8))
    truck2 = Truck(16, 18, truck2_packages, "4001 South 700 East", depart_time=datetime.timedelta(hours=9, minutes=5))
    truck3 = Truck(16, 18, truck3_packages, "4001 South 700 East", depart_time=datetime.timedelta(hours=10, minutes=20))

    # Run delivery simulation using Nearest Neighbor algorithm
    nearest_neighbor(truck1, package_hash, distance_data)
    nearest_neighbor(truck2, package_hash, distance_data)
    nearest_neighbor(truck3, package_hash, distance_data)

    # Start the main program loop
    main()