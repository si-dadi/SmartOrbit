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
import time

# Initial conditions
satellites = []
orbital_positions = []

class SmartOrbitSatellite(Entity):
    def __init__(self, name, semi_major_axis, semi_minor_axis, inclination, raan, argp, fuel_left, priority):
        super().__init__(
            model="models/satellite_model.obj",
            scale=(0.025, 0.025, 0.025),
            render_queue=0,
        )
        self.name = name
        self.semi_major_axis = semi_major_axis
        self.semi_minor_axis = semi_minor_axis
        self.inclination = inclination
        self.raan = raan
        self.argp = argp
        self.fuel_left = fuel_left
        self.priority = priority

        eccentricity = math.sqrt(1 - ((semi_minor_axis * semi_minor_axis) / (semi_major_axis * semi_major_axis)))
        self.orbit = Orbit.from_classical(
            Earth,
            semi_major_axis * u.km,
            eccentricity * u.one,
            inclination * u.deg,
            raan * u.deg,
            argp * u.deg,
            0 * u.deg,
        )

    def update(self):
        dt_factor = getTimeFactor() / 1e5
        dt = time.dt * dt_factor
        self.orbit = self.orbit.propagate(dt * u.s)
        r = (
            self.orbit.r.to(u.km).value / earth.scale_x
        )
        self.position = (
            r[0] * earth.scale_x,
            r[1] * earth.scale_y,
            r[2] * earth.scale_z,
        )
        # print(self.orbit, r, self.position)

def add_smart_orbit_satellite_manual():
    global satellites

    root = tk.Tk()
    root.withdraw()

    dialog = tk.Toplevel(root)
    dialog.title("Enter satellite parameters")
    dialog.geometry("450x350")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - 400) // 2
    y = (screen_height - 200) // 2
    dialog.geometry(f"450x350+{x}+{y}")

    name_label = tk.Label(dialog, text="Name:")
    name_entry = tk.Entry(dialog)
    semi_major_axis_label = tk.Label(dialog, text="Semi-major axis (bw [5,15]):")
    semi_major_axis_entry = tk.Entry(dialog)
    semi_minor_axis_label = tk.Label(dialog, text="Semi-minor axis (bw [5,15]):")
    semi_minor_axis_entry = tk.Entry(dialog)
    inclination_label = tk.Label(dialog, text="Inclination (in degrees):")
    inclination_entry = tk.Entry(dialog)
    raan_label = tk.Label(dialog, text="RAAN (bw [0, 360]):")
    raan_entry = tk.Entry(dialog)
    argp_label = tk.Label(dialog, text="ARGP (bw [0, 360]):")
    argp_entry = tk.Entry(dialog)
    fuel_left_label = tk.Label(dialog, text="Onboard Fuel (bw [0,100] units):")
    fuel_left_entry = tk.Entry(dialog)
    priority_label = tk.Label(dialog, text="Priority (bw [0,5]; Increasing Order):")
    priority_entry = tk.Entry(dialog)

    name_label.grid(row=0, column=0)
    name_entry.grid(row=0, column=1)
    semi_major_axis_label.grid(row=1, column=0)
    semi_major_axis_entry.grid(row=1, column=1)
    semi_minor_axis_label.grid(row=2, column=0)
    semi_minor_axis_entry.grid(row=2, column=1)
    inclination_label.grid(row=3, column=0)
    inclination_entry.grid(row=3, column=1)
    raan_label.grid(row=4, column=0)
    raan_entry.grid(row=4, column=1)
    argp_label.grid(row=5, column=0)
    argp_entry.grid(row=5, column=1)
    fuel_left_label.grid(row=6, column=0)
    fuel_left_entry.grid(row=6, column=1)
    priority_label.grid(row=7, column=0)
    priority_entry.grid(row=7, column=1)

    def submit():
        global name, semi_major_axis, semi_minor_axis, inclination, fuel_left, priority
        name = name_entry.get()
        semi_major_axis = float(semi_major_axis_entry.get())
        semi_minor_axis = float(semi_minor_axis_entry.get())
        inclination = float(inclination_entry.get())
        raan = float(raan_entry.get())
        argp = float(argp_entry.get())
        fuel_left = float(fuel_left_entry.get())
        priority = int(priority_entry.get())

        satellite = SmartOrbitSatellite(
            name, semi_major_axis, semi_minor_axis, inclination, raan, argp, fuel_left, priority
        )
        satellite.parent = universalReferencepoint
        satellites.append(satellite)
        dialog.destroy()
        update_camera_follow_buttons()  # Call the update function here

    def add_smart_orbit_satellite_dummy():
        name = f"Satellite{len(satellites) + 1}"
        semi_major_axis = random.uniform(5, 20)
        semi_minor_axis = random.uniform(5, semi_major_axis)
        inclination = random.uniform(0, 180)
        raan = random.uniform(0, 360)
        argp = random.uniform(0, 360)
        fuel_left = random.uniform(0, 100)
        priority = random.randint(0, 5)

        satellite = SmartOrbitSatellite(
            name, semi_major_axis, semi_minor_axis, inclination, raan, argp, fuel_left, priority
        )
        satellite.parent = (
            universalReferencepoint
        )
        satellites.append(satellite)
        print(
            f"Smart satellite '{name}' added! (semi-major axis: {semi_major_axis}, semi-minor axis: {semi_minor_axis}, inclination: {inclination}, RAAN: {raan}, ARGP: {argp}, fuel left: {fuel_left}, priority: {priority})"
        )
        dialog.destroy()
        update_camera_follow_buttons()  # Call the update function here

    submit_button = tk.Button(dialog, text="Submit", command=submit)
    submit_button.grid(row=8, column=0, columnspan=2)
    or_label = tk.Label(dialog, text="OR")
    or_label.grid(row=9, column=0, columnspan=2)
    randomAdd = tk.Button(
        dialog, text="Add Randomly", command=add_smart_orbit_satellite_dummy
    )
    randomAdd.grid(row=10, column=0, columnspan=2)

    root.wait_window(dialog)

    if "name" in globals():
        satellite = SmartOrbitSatellite(
            name, semi_major_axis, semi_minor_axis, inclination, fuel_left, priority
        )
        satellite.parent = universalReferencepoint
        satellites.append(satellite)
        update_camera_follow_buttons()  # Call the update function here

add_satellite_button = Button(
    text="Add Satellite",
    color=color.gray,
    position=(-0.7, 0.38),
    scale=(0.35, 0.05),
    text_size=5,
    on_click=add_smart_orbit_satellite_manual,
)

cameraShifted = False
following_satellite = None  # Add a variable to track the satellite being followed

def update():
    if cameraShifted and following_satellite:
        camera.position = 2 * following_satellite.position
        # camera.look_at(earth)   # TODO: Fix this
    
    earth.rotation_y -= (
        time.dt * getTimeFactor() * 360 / 86400
    )

def reset_camera():
    global following_satellite, cameraShifted
    following_satellite = None
    camera.position = (0, 0, 0)
    camera.rotation = (0, 0, 0)
    cameraShifted = False

# Initialize camera follow buttons only if there are satellites
camera_follow_buttons = None

def shift_camera_to_satellite(satellite):
    global following_satellite, cameraShifted
    following_satellite = satellite
    cameraShifted = True

def reset_camera():
    global following_satellite, cameraShifted
    following_satellite = None
    camera.position = (0, 0, 0)
    camera.rotation = (0, 0, 0)
    cameraShifted = False

def update_camera_follow_buttons():
    global camera_follow_buttons
    button_list = []

    if satellites:
        for i, satellite in enumerate(satellites):
            follow_button = Button(
                text=f"Follow {satellite.name}",
                color=color.gray,
                position=(-0.7, 0.2 - 0.07 * (i + 1)),  # Offset from "Reset Camera" button
                scale=(0.35, 0.05),
                text_size=5,
                on_click=Func(shift_camera_to_satellite, satellite),
            )
            button_list.append(follow_button)

        # Add the "Reset Camera" button at the top
        reset_button = Button(
            text="Reset Camera",
            color=color.gray,
            position=(-0.7, 0.25),
            scale=(0.35, 0.05),
            text_size=5,
            on_click=reset_camera,
        )
        button_list.append(reset_button)

        if camera_follow_buttons:
            camera_follow_buttons.delete()
        
        camera_follow_buttons = ButtonGroup(options=button_list)

if satellites:
    update_camera_follow_buttons()