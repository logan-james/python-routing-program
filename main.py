


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


def load_packages(filename):
    packages = HashTable()
    with open(filename) as file:
        reader = csv.reader(file)
        for row in reader:
            package_id = int(row[0])
            package = Package(package_id, row[1], row[2], row[3], row[4], row[5], row[6], "At Hub")
            packages.insert(package_id, package)
    return packages


def get_distance(from_address, to_address):
    hub_address = "4001 South 700 East"

    def find_address_index(address):
        if address == "410 S. State St.":
            return next(int(row[0]) for row in address_data if "410 S State St" in row[2])
        try:
            return next(int(row[0]) for row in address_data if address in row[2])
        except StopIteration:
            print(f"Warning: Address '{address}' not found in data. Using hub address instead.")
            return next(int(row[0]) for row in address_data if hub_address in row[2])

    from_idx = find_address_index(from_address)
    to_idx = find_address_index(to_address)

    distance = distance_data[from_idx][to_idx] or distance_data[to_idx][from_idx]
    return float(distance)


def nearest_neighbor(truck, packages, distance_data):
    current_address = truck.current_location
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
            distance = get_distance(current_address, package.get_current_address(truck.current_time))
            delivery_time = datetime.timedelta(hours=distance / truck.speed)

            package.departure_time = truck.depart_time
            package.delivery_time = truck.current_time + delivery_time

            truck.deliver_package(next_package, distance, delivery_time)
            current_address = package.get_current_address(truck.current_time)
        except Exception as e:
            print(f"Error delivering package {next_package}: {e}")
            truck.package_ids.remove(next_package)  # Changed from packages to package_ids



def format_time(time_delta):
    hours, remainder = divmod(time_delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def get_truck_number(package, trucks):
    for truck in trucks:
        if truck.has_package(package.id):
            return truck.id
    return "N/A"


def show_package_status(package_hash, check_time, trucks):
    print(f"\nPackage Status at {format_time(check_time)}:")
    print("-" * 140)
    print(
        f"{'ID':^4} | {'Address':^30} | {'City':^15} | {'State':^5} | {'Zip':^5} | {'Deadline':^10} | {'Weight':^8} | {'Status':^10} | {'Truck':^5} | {'Delivery Time':^15}")
    print("-" * 140)
    for i in range(1, 41):
        package = package_hash.lookup(i)
        if package:
            package.update_status(check_time)
            truck_num = get_truck_number(package, trucks)
            delivery_time = format_time(package.delivery_time) if package.delivery_time else "N/A"
            print(
                f"{package.id:^4} | {package.address:<30} | {package.city:<15} | {package.state:^5} | {package.zipcode:^5} | {package.deadline:^10} | {package.weight:^8} | {package.status:^10} | {truck_num:^5} | {delivery_time:^15}")


def show_truck_packages_status_for_timeframe(truck, package_hash, start_time, end_time):
    print(f"\nPackages status for truck {truck.id} departing at {format_time(truck.depart_time)} between {format_time(start_time)} and {format_time(end_time)}:")
    print("-" * 70)
    print(f"{'Package ID':^10} | {'Status':^15} | {'Delivery Time':^15} | {'Address':^25}")
    print("-" * 70)
    for package_id in truck.all_package_ids:  # Changed from all_packages to all_package_ids
        package = package_hash.lookup(package_id)
        if start_time <= package.delivery_time <= end_time:
            status = "Delivered"
            delivery_time = format_time(package.delivery_time)
        elif package.departure_time <= end_time and (package.delivery_time is None or package.delivery_time > end_time):
            status = "En route"
            delivery_time = "N/A"
        else:
            continue  # Skip packages not relevant to this time frame
        print(f"{package_id:^10} | {status:^15} | {delivery_time:^15} | {package.address:<25}")



def show_total_mileage(trucks):
    print("\nMileage Report:")
    for truck in trucks:
        print(f"Truck {truck.id}: {truck.mileage:.2f} miles")
    total_mileage = sum(truck.mileage for truck in trucks)
    print(f"\nTotal mileage for all trucks: {total_mileage:.2f} miles")


def initialize_trucks(package_hash):
    truck1_packages = [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40]
    truck2_packages = [3, 18, 36, 38]
    truck3_packages = [2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 17, 19, 21, 22, 23, 24, 25, 26, 27, 28, 32, 33, 35, 39]

    truck1 = Truck(1, 16, 18, truck1_packages, "4001 South 700 East", depart_time=datetime.timedelta(hours=8))
    truck2 = Truck(2, 16, 18, truck2_packages, "4001 South 700 East", depart_time=datetime.timedelta(hours=9, minutes=5))
    truck3 = Truck(3, 16, 18, truck3_packages, "4001 South 700 East", depart_time=datetime.timedelta(hours=10, minutes=20))

    return truck1, truck2, truck3


def run_delivery_simulation(truck1, truck2, truck3, package_hash):
    nearest_neighbor(truck1, package_hash, distance_data)
    nearest_neighbor(truck2, package_hash, distance_data)
    nearest_neighbor(truck3, package_hash, distance_data)


def main():
    print("Welcome to WGUPS Package Tracking System")

    package_hash = load_packages("csv/packages.csv")
    truck1, truck2, truck3 = initialize_trucks(package_hash)
    run_delivery_simulation(truck1, truck2, truck3, package_hash)

    trucks = [truck1, truck2, truck3]

    while True:
        print("\nMenu Options:")
        print("1. View status of all packages at a specific time")
        print("2. View status of a specific package")
        print("3. View package status for specific time frame")
        print("4. View total mileage (all trucks and individual)")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            time_input = input("Enter time to check status (HH:MM): ")
            try:
                h, m = map(int, time_input.split(":"))
                check_time = datetime.timedelta(hours=h, minutes=m)
                show_package_status(package_hash, check_time, trucks)
            except ValueError:
                print("Invalid time format. Please use HH:MM.")

        elif choice == '2':
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

            for truck in trucks:
                show_truck_packages_status_for_timeframe(truck, package_hash, start_time, end_time)

        elif choice == '4':
            show_total_mileage(trucks)

        elif choice == '5':
            print("Thank you for using WGUPS Package Tracking System. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()