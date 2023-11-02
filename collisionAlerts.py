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

# Generate 5 random collision messages
def add_collision_alert():
    satellite_A = random.choice(['Satellite X', 'Satellite Y', 'Satellite Z'])
    satellite_B = random.choice(['Satellite P', 'Satellite Q', 'Satellite R'])
    time_seconds = random.randint(180, 220)

    message = f"Collision detected between {satellite_A} and {satellite_B} after roughly {time_seconds} seconds."
    collision_alerts.append(message)
    update_alerts()

    # # Check if a collision was successfully averted (1 in 5 chance)
    # if random.randint(1, 5) == 1:
    #     averted_message = f"Collision successfully averted between {satellite_A} and {satellite_B}."
    #     collision_alerts.append(averted_message)
    #     update_alerts()

# Button to add new collision alerts
add_button = Button(text='Add Collision Alert', scale=(0.25, 0.075), x=0.6, y=0.4, on_click=add_collision_alert, color = color.gray)

update_alerts()  # Initial display of the latest 5 alerts
