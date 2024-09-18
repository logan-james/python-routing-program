# package.py

class Package:
    def __init__(self, package_id, address, city, state, zipcode, deadline, weight, status):
        # Initialize a Package object with all necessary attributes
        self.id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.departure_time = None
        self.delivery_time = None

    # Return a string representation of the Package
    def __str__(self):
        return (f"Package {self.id}: {self.address}, {self.city}, {self.state}, "
                f"{self.zipcode}, {self.deadline}, {self.weight}, {self.status},"
                f" Delivered at: {self.delivery_time}")

    # Update the status of the package based on the current time
    def update_status(self, current_time):
        if self.delivery_time and self.delivery_time <= current_time:
            self.status = "Delivered"
        elif self.departure_time and self.departure_time <= current_time:
            self.status = "En route"
        else:
            self.status = "At Hub"