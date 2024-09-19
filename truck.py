class Truck:
    def __init__(self, id, capacity, speed, package_ids, current_location, mileage=0, depart_time=None):
        self.id = id
        self.capacity = capacity
        self.speed = speed
        self.package_ids = package_ids.copy()
        self.all_package_ids = package_ids.copy()  # Keep track of all packages, including delivered ones
        self.current_location = current_location
        self.mileage = mileage
        self.depart_time = depart_time
        self.current_time = depart_time

    def deliver_package(self, package_id, distance, time):
        self.mileage += distance
        self.current_time += time
        self.package_ids.remove(package_id)
        self.current_location = self.get_package_address(package_id)

    def get_package_address(self, package_id):
        # This method should be implemented to return the address of the package
        # For now, we'll return a placeholder
        return "Package Address"

    def has_package(self, package_id):
        return package_id in self.all_package_ids