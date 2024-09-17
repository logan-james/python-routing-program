class Truck:
    def __init__(self, capacity, speed, packages, current_location, mileage=0, depart_time=None):
        self.capacity = capacity
        self.speed = speed
        self.packages = packages.copy()  # Current packages
        self.all_packages = packages.copy()  # All packages ever loaded
        self.current_location = current_location
        self.mileage = mileage
        self.depart_time = depart_time
        self.current_time = depart_time

    def deliver_package(self, package_id, distance, time):
        self.mileage += distance
        self.current_time += time
        self.packages.remove(package_id)
        print(f"Truck current time: {self.current_time}")  # Debug print