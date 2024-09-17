class Truck:
    def __init__(self, capacity, speed, packages, current_location, mileage=0, depart_time=None):
        # Truck initialization with capacity, speed, and packages
        self.capacity = capacity
        self.speed = speed
        self.packages = packages or []
        self.current_location = current_location
        self.mileage = mileage
        self.depart_time = depart_time
        self.current_time = depart_time

    def __str__(self):
        # Formatted string for truck details
        return f"Truck: Capacity: {self.capacity}, Speed: {self.speed} mph, Packages: {self.packages}, Mileage: {self.mileage} miles, Departed at: {self.depart_time}"

    def deliver_package(self, distance, time):
        # Update truck mileage and current time
        self.mileage += distance
        self.current_time += time
