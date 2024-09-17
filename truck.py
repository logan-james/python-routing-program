# In truck.py
import datetime

class Truck:
    def __init__(self, capacity=16, speed=18, load=None, mileage=0, address="Western Governors University 4001 South 700 East, Salt Lake City, UT 84107", depart_time=None):
        self.capacity = capacity
        self.speed = speed  # in miles per hour
        self.load = load if load else []
        self.mileage = mileage
        self.address = address
        self.depart_time = depart_time if depart_time else datetime.datetime(2023, 5, 8, 8, 0)  # Default to 8:00 AM
        self.current_time = self.depart_time  # Initialize current_time to depart_time

    def add_package(self, package):
        if len(self.load) < self.capacity:
            self.load.append(package)
            return True
        return False

    def remove_package(self, package_id):
        self.load = [pkg for pkg in self.load if pkg != package_id]

    def calculate_travel_time(self, distance):
        return datetime.timedelta(hours=distance / self.speed)