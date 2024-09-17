import datetime

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

class Package:
    def __init__(self, id, address, city, state, zip, deadline, weight, special_notes=""):
        self.id = id
        self.raw_address = address  # Original address from the package file
        # Use the mapped address; default to raw_address if not found in mapping
        self.address = address_mapping.get(address, address)
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.special_notes = special_notes
        self.status = "At hub"
        self.delivery_time = None
        self.pickup_time = None  # Time when the package leaves the hub

    def __str__(self):
        delivery_time_str = self.delivery_time.strftime('%H:%M:%S') if self.delivery_time else 'N/A'
        pickup_time_str = self.pickup_time.strftime('%H:%M:%S') if self.pickup_time else 'N/A'
        return (f"Package {self.id}:\n"
                f"  Address: {self.raw_address}, {self.city}, {self.state} {self.zip}\n"
                f"  Deadline: {self.deadline}\n"
                f"  Weight: {self.weight} kg\n"
                f"  Status: {self.status}\n"
                f"  Pickup Time: {pickup_time_str}\n"
                f"  Delivery Time: {delivery_time_str}\n"
                f"  Notes: {self.special_notes}")

    def update_status(self, status, time):
        self.status = status
        if status == "En route":
            self.pickup_time = time
        elif status == "Delivered":
            self.delivery_time = time

    def update_address(self, new_address):
        self.raw_address = new_address
        self.address = address_mapping.get(new_address, new_address)
        self.city, self.state, self.zip = self._parse_address(new_address)

    def _parse_address(self, address):
        # This is a placeholder method. You'll need to implement proper parsing logic
        # based on the format of your address strings.
        parts = address.split(',')
        if len(parts) >= 3:
            city = parts[-3].strip()
            state = parts[-2].strip()
            zip_code = parts[-1].strip()
            return city, state, zip_code
        return None, None, None

    def _parse_deadline(self, deadline):
        if deadline == "EOD":
            return datetime.time(17, 0)  # 5:00 PM
        return datetime.datetime.strptime(deadline, "%H:%M:%S").time()
