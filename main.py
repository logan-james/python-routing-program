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


# Load the packages CSV file into memory
def load_packages(filename):
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
            # Create a Package object and insert into the hash table
            package = Package(package_id, address, city, state, zipcode, deadline, weight, status)
            packages.insert(package_id, package)
    return packages


def get_distance(from_address, to_address):
    # Get the distance between two addresses using the distance_data
    from_idx = None
    to_idx = None

    # Find indices for both from_address and to_address
    for row in address_data:
        if from_address in row:
            from_idx = int(row[0])
        if to_address in row:
            to_idx = int(row[0])

    # If addresses are not found, raise an error
    if from_idx is None or to_idx is None:
        raise ValueError(f"Address not found: {from_address} or {to_address}")

    # Get the distance from the distance matrix
    distance = distance_data[from_idx][to_idx] or distance_data[to_idx][from_idx]
    return float(distance)


def nearest_neighbor(truck, packages, distance_data):
    # Deliver packages using the nearest neighbor approach
    current_address = truck.current_location
    while truck.packages:
        next_package = min(
            truck.packages, key=lambda p: get_distance(current_address, packages.lookup(p).address)
        )
        distance = get_distance(current_address, packages.lookup(next_package).address)
        delivery_time = datetime.timedelta(hours=distance / truck.speed)
        truck.deliver_package(distance, delivery_time)
        packages.lookup(next_package).delivery_time = truck.current_time
        truck.packages.remove(next_package)
        current_address = packages.lookup(next_package).address


# Initialize the packages and trucks
package_hash = load_packages("csv/packages.csv")

# Define trucks with packages
truck1 = Truck(16, 18, [1, 13, 15], "4001 South 700 East", depart_time=datetime.timedelta(hours=8))
truck2 = Truck(16, 18, [3, 7, 12], "4001 South 700 East", depart_time=datetime.timedelta(hours=9, minutes=30))

# Start delivering packages
nearest_neighbor(truck1, package_hash, distance_data)
nearest_neighbor(truck2, package_hash, distance_data)


# User Interface
def show_package_status(time):
    for i in range(1, 41):
        package = package_hash.lookup(i)
        if package:
            package.update_status(time)
            print(package)


print("Welcome to WGUPS")
while True:
    print("1. Show status of all packages")
    print("2. Show specific package status")
    print("3. Show total mileage")
    print("4. Exit")

    choice = input("Enter choice: ")
    if choice == '1':
        time_input = input("Enter time (HH:MM): ")
        h, m = map(int, time_input.split(":"))
        show_package_status(datetime.timedelta(hours=h, minutes=m))
    elif choice == '2':
        package_id = int(input("Enter package ID: "))
        package = package_hash.lookup(package_id)
        if package:
            time_input = input("Enter time (HH:MM): ")
            h, m = map(int, time_input.split(":"))
            package.update_status(datetime.timedelta(hours=h, minutes=m))
            print(package)
        else:
            print("Package not found.")
    elif choice == '3':
        print(f"Total mileage: {truck1.mileage + truck2.mileage}")
    elif choice == '4':
        break
    else:
        print("Invalid choice. Try again.")
