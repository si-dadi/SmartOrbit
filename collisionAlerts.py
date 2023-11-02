from ursina import *
import random

# app = Ursina()

collision_alerts = []

# Create an Entity to hold the text objects
alert_holder = Draggable(scale=(0.75, 0.2), position=(0,0.35), color=color.clear)

# Create a function to update the collision_alerts and display the latest 5
def update_alerts():
    # print("called me?")
    for child in alert_holder.children:
        destroy(child)  # Remove existing text objects

    for i, alert in enumerate(collision_alerts[-5:]):
        Text(parent=alert_holder, color=color.white, text=alert, y=0.3 - i * 0.15, origin=(0, 0), scale=(1,4))  # Adjust the scale value for text size


update_alerts()  # Initial display of the latest 5 alerts
