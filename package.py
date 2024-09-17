class Package:
    def __init__(self, package_id, address, city, state, zipcode, deadline, weight, status):
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

    def __str__(self):
        # Formatted string for package details
        return f"Package {self.id}: {self.address}, {self.city}, {self.state}, {self.zipcode}, {self.deadline}, {self.weight}, {self.status}, Delivered at: {self.delivery_time}"

    def update_status(self, current_time):
        # Update status based on delivery and departure times
        if self.delivery_time and self.delivery_time < current_time:
            self.status = "Delivered"
        elif self.departure_time and self.departure_time <= current_time:
            self.status = "En Route"
        else:
            self.status = "At Hub"
