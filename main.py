import json
import turtle
import urllib.request
import time
import webbrowser
import geocoder
import os

# Print current directory and files
print("Current working directory:", os.getcwd())
print("Files in the directory:", os.listdir())

# Fetch astronauts currently in space
url = "http://api.open-notify.org/astros.json"
response = urllib.request.urlopen(url)
result = json.loads(response.read())
file = open("iss.txt", "w")
file.write("There are currently " +
           str(result["number"]) + " astronauts on the ISS: \n\n")
people = result['people']
for p in people:
    file.write(p['name'] + " - on board" + "\n")

# Print latitude and longitude
g = geocoder.ip('me')
file.write("\nYour current lat/long is: " + str(g.latlng))
file.close()
webbrowser.open("iss.txt")

# Setup the world map in turtle module
screen = turtle.Screen()
screen.setup(1280, 720)
screen.setworldcoordinates(-180, -90, 180, 90)

# Load the world map image
try:
    screen.bgpic("world-map.gif")
    print("Successfully loaded world-map.gif")
except turtle.TurtleGraphicsError as e:
    print(f"Error loading world-map.gif: {e}")
    screen.bgcolor("lightblue")  # Fallback to a color if image fails to load

# Load the ISS image
try:
    screen.register_shape("iss-icon.gif")
    iss = turtle.Turtle()
    iss.shape("iss-icon.gif")
    print("Successfully loaded iss-icon.gif")
except turtle.TurtleGraphicsError as e:
    print(f"Error loading iss-icon.gif: {e}")
    iss = turtle.Turtle()
    iss.shape("circle")  # Fallback to a circle shape if image fails to load

iss.setheading(45)
iss.penup()

# Main loop to update ISS location
while True: 
    # Fetch the current status of the ISS in real-time
    url = "http://api.open-notify.org/iss-now.json"
    response = urllib.request.urlopen(url)
    result = json.loads(response.read())

    # Extract the ISS location
    location = result["iss_position"]
    lat = location['latitude']
    lon = location['longitude']

    # Output lon and lat to the terminal
    lat = float(lat)
    lon = float(lon)
    print("\nLatitude: " + str(lat))
    print("Longitude: " + str(lon))

    # Update the ISS location on the map
    iss.goto(lon, lat)

    # Refresh each 5 seconds
    time.sleep(5)

# Keep the window open
turtle.done()
