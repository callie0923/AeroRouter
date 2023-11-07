import random
from geopy.distance import geodesic
from json import load
from math import atan2, degrees, radians, sin, cos
import json

# Define a function to calculate initial compass bearing
def calculate_initial_compass_bearing(pointA, pointB):
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = pointA[0]
    lat2 = pointB[0]
    lon1 = pointA[1]
    lon2 = pointB[1]

    if (lat1 == lat2) and (lon1 == lon2):
        return 0

    delta_lon = lon2 - lon1

    x = atan2(
        sin(radians(delta_lon)) * cos(radians(lat2)),
        cos(radians(lat1)) * sin(radians(lat2)) - sin(radians(lat1)) * cos(radians(lat2)) * cos(radians(delta_lon))
    )

    initial_bearing = degrees(x)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing

# Load airport data from the JSON file
with open('airports.json', 'r') as f:
    airport_data = json.load(f)

# Filter airports that belong to the United States
us_airports = [airport for airport in airport_data if airport['country'] == 'United States']

# Extract the airport codes and coordinates for US airports
us_airport_coords = {airport['iata_code']: (float(airport['_geoloc']['lat']), float(airport['_geoloc']['lng'])) for airport in us_airports}

# Load aircraft data from the JSON file
with open('aircraft.json', 'r') as f:
    aircraft_data = json.load(f)

# List to store selected flight options
flight_options = []

# Number of flight options to generate
num_flight_options = 3

for _ in range(num_flight_options):
    # Randomly select an aircraft category
    selected_category = random.choice(list(aircraft_data.keys()))

    # List to store selected legs for this set
    legs = []
    available_airports = list(us_airport_coords.keys())

    # Generate three legs for this set
    for _ in range(3):
        # Randomly select a departure airport
        departure = random.choice(available_airports)

        # Randomly select an arrival airport
        available_airports.remove(departure)
        arrival = random.choice(available_airports)

        # Calculate the distance and magnetic track for this leg
        departure_coords = us_airport_coords[departure]
        arrival_coords = us_airport_coords[arrival]
        distance = geodesic(departure_coords, arrival_coords).nautical
        track = calculate_initial_compass_bearing(departure_coords, arrival_coords)

        # Calculate altitudes based on the distance and magnetic track
        if distance < 25:
            altitude = random.randint(3000, 5000)
        elif 50 <= distance < 100:
            altitude = random.randint(5000, 10000)
        elif 100 <= distance < 500:
            if 1 <= track <= 180:
                altitude = random.choice(range(3000, 41000, 2000))  # Odd altitude
            else:
                altitude = random.choice(range(2000, 41000, 2000))  # Even altitude
        elif 500 <= distance < 2000:
            if 1 <= track <= 180:
                altitude = random.choice(range(3000, 41000, 2000))  # Odd altitude
            else:
                altitude = random.choice(range(2000, 41000, 2000))  # Even altitude
        else:
            if 1 <= track <= 180:
                altitude = random.choice(range(3000, 41000, 2000))  # Odd altitude (default)
            else:
                altitude = random.choice(range(2000, 41000, 2000))  # Even altitude (default)

        # Check if the selected category is A, B, C, or D
        if selected_category in ['Category A Aircraft', 'Category B Aircraft', 'Category C Aircraft', 'Category D Aircraft']:
            # Apply distance restrictions for categories A-D
            if 2000 <= distance <= 5000:
                legs.append((departure, arrival, distance, track, altitude))
            else:
                # If the distance doesn't meet the requirements, switch to another category
                while selected_category in ['Category A Aircraft', 'Category B Aircraft', 'Category C Aircraft', 'Category D Aircraft']:
                    selected_category = random.choice(list(aircraft_data.keys()))
                continue
        else:
            # Use other categories for routes that don't meet the requirements
            legs.append((departure, arrival, distance, track, altitude))

    # Append the selected legs for this set to the flight options list
    flight_options.append((selected_category, legs))

# Export the route as DCT for all legs
route = "DCT"

# Print the selected flight options for all sets
for selected_category, legs in flight_options:
    print(f"Selected Aircraft Category: {selected_category}")
    for departure, arrival, distance, track, altitude in legs:
        print(f"Departure Airport: {departure}")
        print(f"Arrival Airport: {arrival}")
        print(f"Route: {route}")
        print(f"Altitude: FL{altitude // 1000:03d}")
        print(f"Distance: {distance:.2f} nautical miles")
        print(f"Track: {track:.2f} degrees")
    print()