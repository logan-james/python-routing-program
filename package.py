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

    # Returns a string representation of the package object
    def __str__(self):
        return (f"Package {self.id}: {self.address}, {self.city}, {self.state}, "
                f"{self.zipcode}, {self.deadline}, {self.weight}, {self.status},"
                f" Delivered at: {self.delivery_time}")

    # Update the status of the package based on the current time
    def update_status(self, current_time):
        # If the package has been delivered, set status to 'Delivered'
        if self.delivery_time and self.delivery_time <= current_time:
            self.status = "Delivered"
        # If the package has left the hub but is not delivered yet, set status to 'En route'
        elif self.departure_time and self.departure_time <= current_time:
            self.status = "En route"
        # If the package has not left the hub, set status to 'At Hub'
        else:
            self.status = "At Hub"

    # Check and update the address of the package if necessary
    def check_and_update_address(self, current_time):
        # Special update condition for package with ID 9 at 10:20 AM
        update_time = datetime.timedelta(hours=10, minutes=20)
        if self.id == 9:
            # If the current time is after the update time, change the address
            if current_time >= update_time:
                self.address = "410 S. State St."
                self.city = "Salt Lake City"
                self.state = "UT"
                self.zipcode = "84111"
            # Otherwise, keep the original address
            else:
                self.address = self.original_address
                self.city = self.original_city
                self.state = self.original_state
                self.zipcode = self.original_zipcode

    # Return the current address of the package based on the current time
    def get_current_address(self, current_time):
        self.check_and_update_address(current_time)  # Check if address needs to be updated
        return self.address  # Return the current address
