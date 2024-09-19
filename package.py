import datetime

class Package:
    def __init__(self, package_id, address, city, state, zipcode, deadline, weight, status):
        # Initialize package attributes
        self.id = package_id
        self.original_address = address  # Store the original address for potential reversion
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.departure_time = None
        self.delivery_time = None

    # Provide a string representation of the package
    def __str__(self):
        return (f"Package {self.id}: {self.address}, {self.city}, {self.state}, "
                f"{self.zipcode}, {self.deadline}, {self.weight}, {self.status},"
                f" Delivered at: {self.delivery_time}")

    # Update the package status based on the current time
    def update_status(self, current_time):
        if self.delivery_time and self.delivery_time <= current_time:
            self.status = "Delivered"
        elif self.departure_time and self.departure_time <= current_time:
            self.status = "En route"
        else:
            self.status = "At Hub"

    # Update the package's address information
    def update_address(self, new_address, new_city, new_state, new_zipcode):
        self.address = new_address
        self.city = new_city
        self.state = new_state
        self.zipcode = new_zipcode

    # Check and update the address for Package #9 at the specified time
    def check_and_update_address(self, current_time):
        update_time = datetime.timedelta(hours=10, minutes=20)
        if self.id == 9 and current_time >= update_time and self.status != "Delivered":
            # Update to the correct address after 10:20 AM if not yet delivered
            self.update_address("410 S. State St.", "Salt Lake City", "UT", "84111")
        elif self.id == 9 and current_time < update_time:
            # Revert to the original address before 10:20 AM
            self.address = self.original_address

    # Get the current address, updating it if necessary
    def get_current_address(self, current_time):
        self.check_and_update_address(current_time)
        return self.address