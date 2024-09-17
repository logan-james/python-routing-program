# Logan Arguello
# Student ID# 012053764
# C950

import csv
import datetime
from hashmap import HashTable
from package import Package
from truck import Truck

# Load the distances CSV file into memory
with open("csv/distances.csv") as f:
    distance_data = list(csv.reader(f))

# Load the addresses CSV file into memory
with open("csv/addresses.csv") as f:
    address_data = list(csv.reader(f))

def load_packages(filename):
    """
    Load packages from a CSV file into a hash table.
    """
    packages = HashTable()
    with open(filename) as file:
        reader = csv.reader(file)
        for row in reader:
            package_id = int(row[0])
            address = row[1]
            city = row[2]
            state = row[3]
            zipcode = row[4]
            deadline = row[5]
            weight = row[6]
            status = "At Hub"
            package = Package(package_id, address, city, state, zipcode, deadline, weight, status)
            packages.insert(package_id, package)
    return packages

def get_distance(from_address, to_address):
    """
    Calculate the distance between two addresses using the distance data.
    """
    from_idx = None
    to_idx = None
    for row in address_data:
        if from_address in row:
            from_idx = int(row[0])
        if to_address in row:
            to_idx = int(row[0])
    if from_idx is None or to_idx is None:
        raise ValueError(f"Address not found: {from_address} or {to_address}")
    distance = distance_data[from_idx][to_idx] or distance_data[to_idx][from_idx]
    return float(distance)

def nearest_neighbor(truck, packages, distance_data):
    """
    Implement the Nearest Neighbor algorithm for package delivery.
    """
    current_address = truck.current_location
    while truck.packages:
        # Find the nearest undelivered package
        next_package = min(
            truck.packages, key=lambda p: get_distance(current_address, packages.lookup(p).address)
        )
        package = packages.lookup(next_package)
        distance = get_distance(current_address, package.address)
        delivery_time = datetime.timedelta(hours=distance / truck.speed)

        # Update package information
        package.departure_time = truck.depart_time
        package.delivery_time = truck.current_time + delivery_time

        # Deliver the package
        truck.deliver_package(next_package, distance, delivery_time)
        current_address = package.address

def show_truck_packages_status(truck, package_hash, start_time, end_time):
    """
    Display the status of packages on a truck for a given time window.
    """
    print(f"Packages status for truck departing at {truck.depart_time} between {start_time} and {end_time}:")
    for package_id in truck.all_packages:
        package = package_hash.lookup(package_id)
        if package.delivery_time and package.delivery_time <= end_time:
            status = "Delivered"
        elif package.departure_time and start_time <= package.departure_time <= end_time:
            status = "En route"
        elif package.departure_time and package.departure_time < start_time:
            status = "En route"
        else:
            status = "At hub"
        print(f"Package {package_id}: {status}")

def show_total_mileage(trucks):
    """
    Calculate and display the total mileage traveled by all trucks.
    """
    total_mileage = sum(truck.mileage for truck in trucks)
    print(f"Total mileage traveled by all trucks: {total_mileage:.2f}")

def show_package_status(package_hash, time):
    """
    Display the status of all packages at a given time.
    """
    for i in range(1, 41):
        package = package_hash.lookup(i)
        if package:
            package.update_status(time)
            print(package)

# Load packages
package_hash = load_packages("csv/packages.csv")

# Initialize trucks with their assigned packages
truck1_packages = [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40]
truck2_packages = [3, 18, 36, 38]
truck3_packages = [2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 17, 19, 21, 22, 23, 24, 25, 26, 27, 28, 32, 33, 35, 39]

truck1 = Truck(16, 18, truck1_packages, "4001 South 700 East", depart_time=datetime.timedelta(hours=8))
truck2 = Truck(16, 18, truck2_packages, "4001 South 700 East", depart_time=datetime.timedelta(hours=9, minutes=5))
truck3 = Truck(16, 18, truck3_packages, "4001 South 700 East", depart_time=datetime.timedelta(hours=10, minutes=20))

# Run the delivery simulation
nearest_neighbor(truck1, package_hash, distance_data)
nearest_neighbor(truck2, package_hash, distance_data)
nearest_neighbor(truck3, package_hash, distance_data)

# Main program loop
print("Welcome to WGUPS")
while True:
    print("\n1. Show status of all packages")
    print("2. Show specific package status")
    print("3. Show total mileage")
    print("4. Show packages status between 8:35 a.m. and 9:25 a.m.")
    print("5. Show packages status between 9:35 a.m. and 10:25 a.m.")
    print("6. Show packages status between 12:03 p.m. and 1:12 p.m.")
    print("7. Exit")

    choice = input("Enter choice: ")

    if choice == '1':
        time_input = input("Enter time (HH:MM): ")
        h, m = map(int, time_input.split(":"))
        show_package_status(package_hash, datetime.timedelta(hours=h, minutes=m))
    elif choice == '2':
        package_id = int(input("Enter package ID: "))
        time_input = input("Enter time (HH:MM): ")
        h, m = map(int, time_input.split(":"))
        time = datetime.timedelta(hours=h, minutes=m)
        package = package_hash.lookup(package_id)
        if package:
            package.update_status(time)
            print(package)
        else:
            print("Package not found.")
    elif choice == '3':
        show_total_mileage([truck1, truck2, truck3])
    elif choice in ['4', '5', '6']:
        if choice == '4':
            start_time = datetime.timedelta(hours=8, minutes=35)
            end_time = datetime.timedelta(hours=9, minutes=25)
        elif choice == '5':
            start_time = datetime.timedelta(hours=9, minutes=35)
            end_time = datetime.timedelta(hours=10, minutes=25)
        else:
            start_time = datetime.timedelta(hours=12, minutes=3)
            end_time = datetime.timedelta(hours=13, minutes=12)

        show_truck_packages_status(truck1, package_hash, start_time, end_time)
        show_truck_packages_status(truck2, package_hash, start_time, end_time)
        show_truck_packages_status(truck3, package_hash, start_time, end_time)
    elif choice == '7':
        break
    else:
        print("Invalid choice. Try again.")