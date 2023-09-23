from ursina import *
from poliastro.bodies import Earth
from poliastro.twobody import Orbit
from astropy import units as u
import random
import tkinter as tk
from tkinter import simpledialog
from world import *
from timeControl import *
from timeControl import time_factors, current_time_factor_index, getTimeFactor

# Initial conditions
satellites = []
orbital_positions = []

class SmartOrbitSatellite(Entity):
    def __init__(self, name, semi_major_axis, eccentricity, inclination):
        super().__init__(
            model="models/uploads_files_1985975_star+wars.obj",  # Replace with your satellite model
            scale=(0.025, 0.025, 0.025), render_queue=0,
        )
        self.name = name

        # Create an orbit using poliastro
        self.orbit = Orbit.from_classical(
            Earth,
            semi_major_axis * u.km,
            eccentricity * u.one,
            inclination * u.deg,
            0 * u.deg,
            0 * u.deg,
            0 * u.deg,
        )

    def update(self):
        # Propagate the orbit to the current time
        dt_factor = getTimeFactor() / 1e5
        dt = time.dt * dt_factor
        self.orbit = self.orbit.propagate(dt * u.s)
        # print(f"dt_factor: {dt_factor}")
        # Update the position of the satellite
        r = (
            self.orbit.r.to(u.km).value / earth.scale_x
        )  # Convert position to Earth radii
        self.position = (
            r[0] * earth.scale_x,
            r[1] * earth.scale_y,
            r[2] * earth.scale_z,
        )
    print(f"using: {time_factors[current_time_factor_index]}")


class SmartOrbitSatelliteDummy(Entity):
    def __init__(self, name, semi_major_axis, eccentricity, inclination):
        super().__init__(
            model="models/uploads_files_1985975_star+wars.obj",  # Replace with your satellite model
            scale=(0.025, 0.025, 0.025), render_queue=0,
        )
        self.name = name

        # Create an orbit using poliastro
        self.orbit = Orbit.from_classical(
            Earth,
            semi_major_axis * u.km,
            eccentricity * u.one,
            inclination * u.deg,
            0 * u.deg,
            0 * u.deg,
            0 * u.deg,
        )

    def update(self):
        # Propagate the orbit to the current time
        dt_factor = getTimeFactor() / 1e5
        dt = time.dt * dt_factor
        self.orbit = self.orbit.propagate(dt * u.s)
        # print(f"dt_factor: {dt_factor}")
        # Update the position of the satellite
        r = (
            self.orbit.r.to(u.km).value / earth.scale_x
        )  # Convert position to Earth radii
        self.position = (
            r[0] * earth.scale_x,
            r[1] * earth.scale_y,
            r[2] * earth.scale_z,
        )
    print(f"using: {time_factors[current_time_factor_index]}")


def add_smart_orbit_satellite_manual():
    global satellites
    # Create a new tkinter root window
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Create a custom dialog
    dialog = tk.Toplevel(root)
    dialog.title("Enter satellite parameters")
    dialog.geometry("400x200")
    # Calculate the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - 400) // 2
    y = (screen_height - 200) // 2
    dialog.geometry(f"400x200+{x}+{y}")

    # Create input fields
    name_label = tk.Label(dialog, text="Name:")
    name_entry = tk.Entry(dialog)
    semi_major_axis_label = tk.Label(dialog, text="Semi-major axis (bw [5,15]):")
    semi_major_axis_entry = tk.Entry(dialog)
    eccentricity_label = tk.Label(dialog, text="Eccentricity:")
    eccentricity_entry = tk.Entry(dialog)
    inclination_label = tk.Label(dialog, text="Inclination (in degrees):")
    inclination_entry = tk.Entry(dialog)

    # Arrange input fields in a grid
    name_label.grid(row=0, column=0)
    name_entry.grid(row=0, column=1)
    semi_major_axis_label.grid(row=1, column=0)
    semi_major_axis_entry.grid(row=1, column=1)
    eccentricity_label.grid(row=2, column=0)
    eccentricity_entry.grid(row=2, column=1)
    inclination_label.grid(row=3, column=0)
    inclination_entry.grid(row=3, column=1)

    # Create a submit button
    def submit():
        global name, semi_major_axis, eccentricity, inclination
        name = name_entry.get()
        semi_major_axis = float(semi_major_axis_entry.get())
        eccentricity = float(eccentricity_entry.get())
        inclination = float(inclination_entry.get())
        satellite.parent = universalReferencepoint   # Add the satellite as a child of the Earth entity
        dialog.destroy()
    
    def add_smart_orbit_satellite_dummy():
        # Generate random orbital parameters
        name = f"Satellite{len(satellites) + 1}"
        semi_major_axis = random.uniform(5, 20)
        eccentricity = random.uniform(0, 0.75)
        inclination = random.uniform(0, 180)

        # Create the satellite with the random parameters
        satellite = SmartOrbitSatellite(name, semi_major_axis, eccentricity, inclination)
        satellite.parent = universalReferencepoint   # Add the satellite as a child of the Earth entity
        satellites.append(satellite)
        update_satellite_buttons()
        # print(satellites)
        print(f"Smart satellite '{name}' added! (semi-major axis: {semi_major_axis} km, eccentricity: {eccentricity}, inclination: {inclination} degrees)")
        dialog.destroy()

    submit_button = tk.Button(dialog, text="Submit", command=submit)
    submit_button.grid(row=4, column=0, columnspan=2)
    or_label = tk.Label(dialog, text="OR")
    or_label.grid(row=5, column=0, columnspan=2)
    randomAdd = tk.Button(dialog, text="Add Randomly", command=add_smart_orbit_satellite_dummy)
    randomAdd.grid(row=6, column=0, columnspan=2)

    # Wait for the dialog to be destroyed
    root.wait_window(dialog)

    # Check if the dialog was submitted
    if 'name' in globals():
        # Create the satellite with the user's input
        satellite = SmartOrbitSatellite(name, semi_major_axis, eccentricity, inclination)
        satellite.parent = universalReferencepoint
        satellites.append(satellite)
        update_satellite_names()

# Create a button to add a Smart Orbit Satellite
smart_button = Button(
    text="Add Satellite",
    color=color.gray,
    position=(-0.7, 0.38),
    scale=(0.35, 0.05),
    text_size=5,
    on_click=add_smart_orbit_satellite_manual,
)

panel = WindowPanel(
    title="SmartOrbit Satellites",
    content=(
        Text("Click one to shift to its POV!", text_size=5),
        ButtonList(button_dict={}, sub_element_args={"color": color.light_gray}),
    ),
    draggable=True,
    resizable=True,
    min_width=200,
    max_width=400,
    min_height=300,
    max_height=400,
    background_color=color.rgba(255, 255, 255, 0.25),
)

# Function to update the displayed satellite names and buttons
def update_satellite_buttons():
    button_list = panel.content[1].content[0]  # Access the ButtonList element
    button_list.clear()
    for satellite_name, satellite_entity in satellites:
        button = Button(
            text=satellite_name,
            color=color.light_gray,
            on_click=shift_camera_to_satellite,
            args=[satellite_entity],
        )
        button.tooltip = Tooltip(f"View {satellite_name}")
        button_list.append(button)


def shift_camera_to_satellite(satellite_entity):
    camera.position = satellite_entity.position + (0, 0, 5)
    camera.look_at(satellite_entity.position)

# Function to reset the camera position to (0, 0, 0)
def reset_camera():
    camera.position = (0, 0, 0)
    camera.rotation = (0, 0, 0)

reset_camera_button = Button(
    parent=panel.content[0],
    text="Reset Camera",
    scale=(0.3, 0.1),
    on_click=reset_camera,
    position=(0,0)
)
reset_camera_button.tooltip = Tooltip("Reset Camera Position")

