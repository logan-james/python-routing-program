import datetime

class Package:
    def __init__(self, package_id, address, city, state, zipcode, deadline, weight, status):
        # Initialize package attributes
        self.id = package_id
        self.original_address = address
        self.address = address
        self.original_city = city
        self.city = city
        self.original_state = state
        self.state = state
        self.original_zipcode = zipcode
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.departure_time = None
        self.delivery_time = None

    def __str__(self):
        return (f"Package {self.id}: {self.address}, {self.city}, {self.state}, "
                f"{self.zipcode}, {self.deadline}, {self.weight}, {self.status},"
                f" Delivered at: {self.delivery_time}")

    def update_status(self, current_time):
        if self.delivery_time and self.delivery_time <= current_time:
            self.status = "Delivered"
        elif self.departure_time and self.departure_time <= current_time:
            self.status = "En route"
        else:
            self.status = "At Hub"

    def check_and_update_address(self, current_time):
        update_time = datetime.timedelta(hours=10, minutes=20)
        if self.id == 9:
            if current_time >= update_time:
                self.address = "410 S. State St."
                self.city = "Salt Lake City"
                self.state = "UT"
                self.zipcode = "84111"
            else:
                self.address = self.original_address
                self.city = self.original_city
                self.state = self.original_state
                self.zipcode = self.original_zipcode

    def get_current_address(self, current_time):
        self.check_and_update_address(current_time)
        return self.address