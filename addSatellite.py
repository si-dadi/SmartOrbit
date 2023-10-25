from ursina import *
from ursina.shaders import lit_with_shadows_shader
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
from poliastro.bodies import Earth
from poliastro.twobody import Orbit
from astropy import units as u
import random
import tkinter as tk
from tkinter import simpledialog
from world import *
from timeControl import *
from timeControl import time_factors, current_time_factor_index, getTimeFactor
import math

# Initial conditions
satellites = []
orbital_positions = []


class SmartOrbitSatellite(Entity):
    def __init__(self, name, semi_major_axis, semi_minor_axis, inclination, fuel_left, priority):
        super().__init__(
            model="models/satellite_model.obj",
            scale=(0.025, 0.025, 0.025),
            render_queue=0,
        )
        self.name = name
        self.semi_major_axis = semi_major_axis
        self.semi_minor_axis = semi_minor_axis
        self.inclination = inclination
        self.fuel_left = fuel_left
        self.priority = priority

        eccentricity = math.sqrt(1 - (semi_minor_axis ** 2 / semi_major_axis ** 2))
        c = semi_major_axis * math.sqrt(1 - eccentricity**2)
        # x_foci = c * math.sin(self.inclination)
        # z_foci = c * math.cos(self.inclination)
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

        self.orbit_circle = Entity(
            model=Circle(500, mode="line", thickness=1),
            color=color.gray,
            scale=(
                2 * self.semi_major_axis,
                2 * self.semi_minor_axis,
            ),
            shader=lit_with_shadows_shader,
            parent=universalReferencepoint,  # Make the satellite the parent of the orbit circle
            rotation=(90, 0, 0),
            position=(c-semi_major_axis, 0, 0)
        )
        self.orbit_circle.rotation_x = -inclination

    def update(self):
        # Propagate the orbit to the current time
        dt_factor = getTimeFactor() / 1e5
        dt = time.dt * dt_factor
        self.orbit = self.orbit.propagate(dt * u.s)
        # Update the position of the satellite
        r = (
            self.orbit.r.to(u.km).value / earth.scale_x
        )  # Convert position to Earth radii
        self.position = (
            r[0] * earth.scale_x,
            r[1] * earth.scale_y,
            r[2] * earth.scale_z,
        )
        # Adjust the position and rotation of the orbit circle
        # self.orbit_circle.position = (x_foci, 0, z_foci)  # Center it at the focus
        # self.orbit_circle.rotation_z = self.inclination  # Set the inclination


def add_smart_orbit_satellite_manual():
    global satellites
    # Create a new tkinter root window
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Create a custom dialog
    dialog = tk.Toplevel(root)
    dialog.title("Enter satellite parameters")
    dialog.geometry("450x250")
    # Calculate the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - 400) // 2
    y = (screen_height - 200) // 2
    dialog.geometry(f"450x250+{x}+{y}")

    # Create input fields
    name_label = tk.Label(dialog, text="Name:")
    name_entry = tk.Entry(dialog)
    semi_major_axis_label = tk.Label(dialog, text="Semi-major axis (bw [5,15]):")
    semi_major_axis_entry = tk.Entry(dialog)
    semi_minor_axis_label = tk.Label(dialog, text="Semi-minor axis (bw [5,15]):")
    semi_minor_axis_entry = tk.Entry(dialog)
    inclination_label = tk.Label(dialog, text="Inclination (in degrees):")
    inclination_entry = tk.Entry(dialog)
    fuel_left_label = tk.Label(dialog, text="Onboard Fuel (bw [0,100] units):")
    fuel_left_entry = tk.Entry(dialog)
    priority_label = tk.Label(dialog, text="Priority (bw [0,5]; Increasing Order):")
    priority_entry = tk.Entry(dialog)

    # Arrange input fields in a grid
    name_label.grid(row=0, column=0)
    name_entry.grid(row=0, column=1)
    semi_major_axis_label.grid(row=1, column=0)
    semi_major_axis_entry.grid(row=1, column=1)
    semi_minor_axis_label.grid(row=2, column=0)
    semi_minor_axis_entry.grid(row=2, column=1)
    inclination_label.grid(row=3, column=0)
    inclination_entry.grid(row=3, column=1)
    fuel_left_label.grid(row=4, column=0)
    fuel_left_entry.grid(row=4, column=1)
    priority_label.grid(row=5, column=0)
    priority_entry.grid(row=5, column=1)

    # Create a submit button
    def submit():
        global name, semi_major_axis, semi_minor_axis, inclination, fuel_left, priority
        name = name_entry.get()
        semi_major_axis = float(semi_major_axis_entry.get())
        semi_minor_axis = float(semi_minor_axis_entry.get())
        inclination = float(inclination_entry.get())
        fuel_left = float(fuel_left_entry.get())
        priority = int(priority_entry.get())

        satellite = SmartOrbitSatellite(
            name, semi_major_axis, semi_minor_axis, inclination, fuel_left, priority
        )
        satellite.parent = universalReferencepoint
        satellites.append(satellite)
        dialog.destroy()

    def add_smart_orbit_satellite_dummy():
        # Generate random orbital parameters
        name = f"Satellite{len(satellites) + 1}"
        semi_major_axis = random.uniform(5, 20)
        semi_minor_axis = random.uniform(5,semi_major_axis)
        inclination = random.uniform(0, 180)
        fuel_left = random.uniform(0,100)
        priority = random.randint(0,5)

        # Create the satellite with the random parameters
        satellite = SmartOrbitSatellite(
            name, semi_major_axis, semi_minor_axis, inclination, fuel_left, priority
        )
        satellite.parent = (
            universalReferencepoint  # Add the satellite as a child of the Earth entity
        )
        satellites.append(satellite)
        # print(satellites)
        print(
            f"Smart satellite '{name}' added! (semi-major axis: {semi_major_axis} km, semi-minor axis: {semi_minor_axis}, inclination: {inclination} degrees)"
        )
        dialog.destroy()

    submit_button = tk.Button(dialog, text="Submit", command=submit)
    submit_button.grid(row=6, column=0, columnspan=2)
    or_label = tk.Label(dialog, text="OR")
    or_label.grid(row=7, column=0, columnspan=2)
    randomAdd = tk.Button(
        dialog, text="Add Randomly", command=add_smart_orbit_satellite_dummy
    )
    randomAdd.grid(row=8, column=0, columnspan=2)

    # Wait for the dialog to be destroyed
    root.wait_window(dialog)

    # Check if the dialog was submitted
    if "name" in globals():
        # Create the satellite with the user's input
        satellite = SmartOrbitSatellite(
            name, semi_major_axis, semi_minor_axis, inclination, fuel_left, priority
        )
        satellite.parent = universalReferencepoint
        satellites.append(satellite)


# Create a button to add a Smart Orbit Satellite
smart_button = Button(
    text="Add Satellite",
    color=color.gray,
    position=(-0.7, 0.38),
    scale=(0.35, 0.05),
    text_size=5,
    on_click=add_smart_orbit_satellite_manual,
)


def reset_camera():
    camera.position = (0, 0, 0)
    camera.rotation = (0, 0, 0)
