# Logan Arguello ID #012053764

import datetime
from package import Package
from hash_table import HashTable
from distance_data import DistanceData
from truck import Truck

address_mapping = {
   "195 W Oakland Ave": "South Salt Lake Public Works 195 W Oakland Ave",
   "2530 S 500 E": "Columbus Library 2530 S 500 E",
   "233 Canyon Rd": "Salt Lake City Ottinger Hall 233 Canyon Rd",
   "380 W 2880 S": "Utah DMV Administrative Office 380 W 2880 S",
   "410 S State St": "Third District Juvenile Court 410 S State St",
   "3060 Lester St": "Redwood Park 3060 Lester St",
   "1330 2100 S": "Sugar House Park 1330 2100 S",
   "300 State St": "Council Hall 300 State St",
   "600 E 900 South": "Rice Terrace Pavilion Park 600 E 900 South",
   "2600 Taylorsville Blvd": "Taylorsville City Hall 2600 Taylorsville Blvd",
   "3575 W Valley Central Station bus Loop": "West Valley Prosecutor 3575 W Valley Central Sta bus Loop",
   "2010 W 500 S": "Salt Lake City Streets and Sanitation 2010 W 500 S",
   "4300 S 1300 E": "Cottonwood Regional Softball Complex 4300 S 1300 E",
   "4580 S 2300 E": "Holiday City Office 4580 S 2300 E",
   "3148 S 1100 W": "Salt Lake County Mental Health 3148 S 1100 W",
   "1488 4800 S": "Taylorsville-Bennion Heritage City Gov Off 1488 4800 S",
   "177 W Price Ave": "Salt Lake City Division of Health Services 177 W Price Ave",
   "3595 Main St": "Housing Auth. of Salt Lake County 3595 Main St",
   "6351 South 900 East": "Wheeler Historic Farm 6351 South 900 East",
   "5100 South 2700 West": "Valley Regional Softball Complex 5100 South 2700 West",
   "5025 State St": "Murray City Museum 5025 State St",
   "5383 South 900 East #104": "City Center of Rock Springs 5383 South 900 East #104",
   "2835 Main St": "South Salt Lake Police 2835 Main St",
   "3365 S 900 W": "Salt Lake County/United Police Dept 3365 S 900 W",
   "2300 Parkway Blvd": "Deker Lake 2300 Parkway Blvd",
   "1060 Dalton Ave S": "International Peace Gardens 1060 Dalton Ave S",
   "4001 South 700 East": "Western Governors University 4001 South 700 East, Salt Lake City, UT 84107",
}

# Initialize global variables
package_hash = HashTable()
distance_data = DistanceData()
trucks = [Truck(), Truck(), Truck()]

def load_package_data():
    # Load package data from the WGUPS Package File
    packages = [
        Package(1, "195 W Oakland Ave", "Salt Lake City", "UT", "84115", "10:30:00", 21),
        Package(2, "2530 S 500 E", "Salt Lake City", "UT", "84106", "EOD", 44),
        Package(3, "233 Canyon Rd", "Salt Lake City", "UT", "84103", "EOD", 2, "Can only be on truck 2"),
        Package(4, "380 W 2880 S", "Salt Lake City", "UT", "84115", "EOD", 4),
        Package(5, "410 S State St", "Salt Lake City", "UT", "84111", "EOD", 5),
        Package(6, "3060 Lester St", "West Valley City", "UT", "84119", "10:30:00", 88,
                "Delayed on flight---will not arrive to depot until 9:05 am"),
        Package(7, "1330 2100 S", "Salt Lake City", "UT", "84106", "EOD", 8),
        Package(8, "300 State St", "Salt Lake City", "UT", "84103", "EOD", 9),
        Package(9, "300 State St", "Salt Lake City", "UT", "84103", "EOD", 2, "Wrong address listed"),
        Package(10, "600 E 900 South", "Salt Lake City", "UT", "84105", "EOD", 1),
        Package(11, "2600 Taylorsville Blvd", "Salt Lake City", "UT", "84118", "EOD", 1),
        Package(12, "3575 W Valley Central Station bus Loop", "West Valley City", "UT", "84119", "EOD", 1),
        Package(13, "2010 W 500 S", "Salt Lake City", "UT", "84104", "10:30:00", 2),
        Package(14, "4300 S 1300 E", "Millcreek", "UT", "84117", "10:30:00", 88, "Must be delivered with 15, 19"),
        Package(15, "4580 S 2300 E", "Holladay", "UT", "84117", "09:00:00", 4),
        Package(16, "4580 S 2300 E", "Holladay", "UT", "84117", "10:30:00", 88, "Must be delivered with 13, 19"),
        Package(17, "3148 S 1100 W", "Salt Lake City", "UT", "84119", "EOD", 2),
        Package(18, "1488 4800 S", "Salt Lake City", "UT", "84123", "EOD", 6, "Can only be on truck 2"),
        Package(19, "177 W Price Ave", "Salt Lake City", "UT", "84115", "EOD", 37),
        Package(20, "3595 Main St", "Salt Lake City", "UT", "84115", "10:30:00", 37, "Must be delivered with 13, 15"),
        Package(21, "3595 Main St", "Salt Lake City", "UT", "84115", "EOD", 3),
        Package(22, "6351 South 900 East", "Murray", "UT", "84121", "EOD", 2),
        Package(23, "5100 South 2700 West", "Salt Lake City", "UT", "84118", "EOD", 5),
        Package(24, "5025 State St", "Murray", "UT", "84107", "EOD", 7),
        Package(25, "5383 South 900 East #104", "Salt Lake City", "UT", "84117", "10:30:00", 7,
                "Delayed on flight---will not arrive to depot until 9:05 am"),
        Package(26, "5383 South 900 East #104", "Salt Lake City", "UT", "84117", "EOD", 25),
        Package(27, "1060 Dalton Ave S", "Salt Lake City", "UT", "84104", "EOD", 5),
        Package(28, "2835 Main St", "Salt Lake City", "UT", "84115", "EOD", 7,
                "Delayed on flight---will not arrive to depot until 9:05 am"),
        Package(29, "1330 2100 S", "Salt Lake City", "UT", "84106", "10:30:00", 2),
        Package(30, "300 State St", "Salt Lake City", "UT", "84103", "10:30:00", 1),
        Package(31, "3365 S 900 W", "Salt Lake City", "UT", "84119", "10:30:00", 1),
        Package(32, "3365 S 900 W", "Salt Lake City", "UT", "84119", "EOD", 1,
                "Delayed on flight---will not arrive to depot until 9:05 am"),
        Package(33, "2530 S 500 E", "Salt Lake City", "UT", "84106", "EOD", 1),
        Package(34, "4580 S 2300 E", "Holladay", "UT", "84117", "10:30:00", 2),
        Package(35, "1060 Dalton Ave S", "Salt Lake City", "UT", "84104", "EOD", 88),
        Package(36, "2300 Parkway Blvd", "West Valley City", "UT", "84119", "EOD", 88, "Can only be on truck 2"),
        Package(37, "410 S State St", "Salt Lake City", "UT", "84111", "10:30:00", 2),
        Package(38, "410 S State St", "Salt Lake City", "UT", "84111", "EOD", 9, "Can only be on truck 2"),
        Package(39, "2010 W 500 S", "Salt Lake City", "UT", "84104", "EOD", 9),
        Package(40, "380 W 2880 S", "Salt Lake City", "UT", "84115", "10:30:00", 45),
    ]


    for package in packages:
        package_hash.insert(package.id, package)

def get_nearest_package(truck, current_address, current_time):
    nearest_package = None
    min_distance = float('inf')
    packages_available_later = False

    for package_id in truck.load:
        package = package_hash.lookup(package_id)
        if "Delayed" in package.special_notes and current_time < datetime.datetime(2023, 5, 8, 9, 5):
            packages_available_later = True
            continue
        if package.id == 9 and current_time < datetime.datetime(2023, 5, 8, 10, 20):
            packages_available_later = True
            continue
        distance = distance_data.get_distance(current_address, package.address)
        if distance < min_distance:
            min_distance = distance
            nearest_package = package
    return nearest_package, packages_available_later

def deliver_package(truck, package):
    distance = distance_data.get_distance(truck.address, package.address)
    truck.mileage += distance
    travel_time = datetime.timedelta(hours=distance / truck.speed)
    truck.current_time += travel_time
    package.update_status("Delivered", truck.current_time)
    truck.address = package.address
    truck.load.remove(package.id)
    print(f"Delivered package {package.id} at {truck.current_time.strftime('%H:%M:%S')}")

def update_truck_status(truck):
    if not truck.load:
        print(f"Truck is empty at {truck.current_time.strftime('%H:%M:%S')}")

def return_to_hub(truck, hub_address):
    distance = distance_data.get_distance(truck.address, hub_address)
    truck.mileage += distance
    time_delta = datetime.timedelta(hours=distance / truck.speed)
    truck.current_time += time_delta
    truck.address = hub_address
    print(f"Truck returned to hub at {truck.current_time.strftime('%H:%M:%S')}")
    return truck.current_time

def load_trucks():
    # First driver leaves with Truck 1 at 8:00 AM
    trucks[0].load = [13, 14, 15, 16, 19, 20, 29, 34, 40]  # Adjusted packages
    trucks[0].depart_time = datetime.datetime(2023, 5, 8, 8, 0)

    # Second driver leaves with Truck 2 at 8:00 AM
    trucks[1].load = [3, 18, 36, 38, 6, 25, 28, 32]  # Delayed packages will be handled in logic
    trucks[1].depart_time = datetime.datetime(2023, 5, 8, 8, 0)

    # First driver takes Truck 1 again after returning to hub
    trucks[2].load = [1, 2, 4, 5, 7, 8, 9, 10, 11, 12, 17, 21, 22, 23, 24, 26, 27, 30, 31, 33, 35, 37, 39]
    trucks[2].depart_time = datetime.datetime(2023, 5, 8, 9, 5)

def deliver_packages():
    hub_address = "Western Governors University 4001 South 700 East, Salt Lake City, UT 84107"

    for truck_index, truck in enumerate(trucks):
        truck.current_time = truck.depart_time
        current_address = hub_address

        while truck.load:
            nearest_package, packages_available_later = get_nearest_package(truck, current_address, truck.current_time)

            if nearest_package is None:
                if packages_available_later:
                    next_available_times = []
                    for package_id in truck.load:
                        package = package_hash.lookup(package_id)
                        if "Delayed" in package.special_notes:
                            next_available_times.append(datetime.datetime(2023, 5, 8, 9, 5))
                        if package.id == 9:
                            next_available_times.append(datetime.datetime(2023, 5, 8, 10, 20))
                    truck.current_time = max(truck.current_time, min(next_available_times))
                    continue
                else:
                    break

            if nearest_package.id == 9 and truck.current_time >= datetime.datetime(2023, 5, 8, 10, 20):
                corrected_address = "410 S State St"
                nearest_package.update_address(address_mapping.get(corrected_address, corrected_address))

            deliver_package(truck, nearest_package)
            update_truck_status(truck)
            current_address = nearest_package.address

        truck.current_time = return_to_hub(truck, hub_address)

        print(f"Truck {truck_index + 1} total distance: {truck.mileage:.1f} miles, Finish time: {truck.current_time.strftime('%H:%M:%S')}")

    total_mileage = sum(truck.mileage for truck in trucks)
    print(f"Total distance for all trucks: {total_mileage:.1f} miles")

def check_package_status(package_id, time):
    package = package_hash.lookup(package_id)
    if package:
        if package.delivery_time and package.delivery_time <= time:
            status = f"Delivered at {package.delivery_time.strftime('%H:%M:%S')}"
        elif package.pickup_time and package.pickup_time <= time:
            status = f"En route (Left at {package.pickup_time.strftime('%H:%M:%S')})"
        else:
            status = "At hub"
        return f"Package {package_id} status: {status}"
    return f"Package {package_id} not found"


def generate_report(check_time):
    all_packages = package_hash.get_all_packages()
    delivered = []
    en_route = []
    at_hub = []

    for package in all_packages:
        if package.delivery_time and package.delivery_time <= check_time:
            delivered.append(package)
        elif package.pickup_time and package.pickup_time <= check_time:
            en_route.append(package)
        else:
            at_hub.append(package)

    print(f"\nStatus Report at {check_time.strftime('%H:%M:%S')}:")
    print(f"Delivered: {len(delivered)} packages")
    print(f"En route: {len(en_route)} packages")
    print(f"At hub: {len(at_hub)} packages")

    return delivered, en_route, at_hub

def user_interface():
    while True:
        print("\nWGUPS Package Tracking System")
        print("1. Check all package statuses")
        print("2. Check a single package status at a specific time")
        print("3. Check all package statuses at a specific time")
        print("4. View total mileage traveled by all trucks")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            all_packages = package_hash.get_all_packages()
            for package in all_packages:
                print(package)
        elif choice == '2':
            try:
                package_id = int(input("Enter package ID (1-40): "))
                if not 1 <= package_id <= 40:
                    print("Invalid package ID. Please enter a number between 1 and 40.")
                    continue
                time_str = input("Enter time (HH:MM:SS): ")
                hour, minute, second = map(int, time_str.split(':'))
                check_time = datetime.datetime(2023, 5, 8, hour, minute, second)
                print(check_package_status(package_id, check_time))
            except ValueError:
                print("Invalid input. Please try again.")
        elif choice == '3':
            try:
                time_str = input("Enter time (HH:MM:SS): ")
                hour, minute, second = map(int, time_str.split(':'))
                check_time = datetime.datetime(2023, 5, 8, hour, minute, second)
                all_packages = package_hash.get_all_packages()
                delivered = 0
                en_route = 0
                at_hub = 0
                for package in all_packages:
                    status = check_package_status(package.id, check_time)
                    print(status)
                    if "Delivered" in status:
                        delivered += 1
                    elif "En route" in status:
                        en_route += 1
                    else:
                        at_hub += 1
                print(f"\nSummary at {check_time.strftime('%H:%M:%S')}:")
                print(f"Delivered: {delivered} packages")
                print(f"En route: {en_route} packages")
                print(f"At hub: {at_hub} packages")
            except ValueError:
                print("Invalid input. Please try again.")
        elif choice == '4':
            total_mileage = sum(truck.mileage for truck in trucks)
            print(f"Total mileage traveled by all trucks: {total_mileage:.1f} miles")
        elif choice == '5':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

def verify_addresses():
    missing_addresses = []
    for package_id in range(1, 41):
        package = package_hash.lookup(package_id)
        if package.address not in distance_data.addresses:
            missing_addresses.append((package_id, package.address))
    if missing_addresses:
        print("The following packages have addresses not found in distance data:")
        for package_id, address in missing_addresses:
            print(f"Package {package_id}: {address}")
    else:
        print("All package addresses are valid.")

if __name__ == "__main__":
    load_package_data()
    load_trucks()
    verify_addresses()  # Verify addresses before starting deliveries
    deliver_packages()
    user_interface()