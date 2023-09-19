from ursina import *
from poliastro.bodies import Earth
from poliastro.twobody import Orbit
from astropy import units as u
import random
import tkinter as tk
from tkinter import simpledialog

app = Ursina()

window.title = "SafeOrbit"
window.borderless = False
window.exit_button.visible = False
window.fps_counter.enabled = True

camera = EditorCamera(
    rotation_speed=100,
    pan_speed=(0.5, 0.5),
    zoom_speed=1,
    position=(0, 0, 0),
    target=(0, 0, 0),
)

earth_texture = load_texture("textures/wallpaperflare.com_wallpaper (2).jpg")
earth = Entity(
    model="sphere",
    texture=earth_texture,
    scale=2,
    subdivisions=256,
    position=(0, 0, 0),
)

sun_light = DirectionalLight(color=color.white, y=2, z=-3, shadows=True)
sun_light.rotation = (10, 30, 30)

sky_texture = load_texture("textures/black-color-solid-background-1920x1080.png")
sky = Entity(model="sphere", texture=sky_texture, scale=1000, double_sided=True)
sky.shader = "unlit"

# Constants
G = 6.67430e-11  # Gravitational constant (m^3/kg/s^2)
earth_mass = 5.972e24  # Earth's mass (kg)

# Initial conditions
satellites = []
orbital_positions = []

universalReferencepoint = Entity(
    model="sphere", x=0, y=0, z=0, scale=1.9, color=color.black
)


class SmartOrbitSatellite(Entity):
    def __init__(self, name, semi_major_axis, eccentricity, inclination):
        super().__init__(
            model="models/uploads_files_1985975_star+wars.obj",  # Replace with your satellite model
            scale=(0.025, 0.025, 0.025),
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
        dt_factor = (
            time_factors[current_time_factor_index] / 1e5
        )  # time factor to speed up the simulation
        dt = time.dt * dt_factor
        self.orbit = self.orbit.propagate(dt * u.s)

        # Update the position of the satellite
        r = (
            self.orbit.r.to(u.km).value / earth.scale_x
        )  # Convert position to Earth radii
        self.position = (r[0], r[1], r[2])

class SmartOrbitSatelliteDummy(Entity):
    def __init__(self, name, semi_major_axis, eccentricity, inclination):
        super().__init__(
            model="models/uploads_files_1985975_star+wars.obj",  # Replace with your satellite model
            scale=(0.025, 0.025, 0.025),
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
        dt_factor = (
            time_factors[current_time_factor_index] / 1e5
        )  # time factor to speed up the simulation
        dt = time.dt * dt_factor
        self.orbit = self.orbit.propagate(dt * u.s)

        # Update the position of the satellite
        r = (
            self.orbit.r.to(u.km).value / earth.scale_x
        )  # Convert position to Earth radii
        self.position = (r[0], r[1], r[2])



def add_smart_orbit_satellite_manual():
    # Create a new tkinter root window
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Create a custom dialog
    dialog = tk.Toplevel(root)
    dialog.title("Enter satellite parameters")

    # Create input fields
    name_label = tk.Label(dialog, text="Name:")
    name_entry = tk.Entry(dialog)
    semi_major_axis_label = tk.Label(dialog, text="Semi-major axis (in km):")
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
        eccentricity = random.uniform(0.5, 1)
        inclination = random.uniform(0, 180)

        # Create the satellite with the random parameters
        satellite = SmartOrbitSatelliteDummy(name, semi_major_axis, eccentricity, inclination)
        satellite.parent = universalReferencepoint   # Add the satellite as a child of the Earth entity
        satellites.append(satellite)

        print(f"Smart satellite '{name}' added! (semi-major axis: {semi_major_axis} km, eccentricity: {eccentricity}, inclination: {inclination} degrees)")
        dialog.destroy()

    submit_button = tk.Button(dialog, text="Submit", command=submit)
    submit_button.grid(row=4, columnspan=2)
    randomAdd = tk.Button(dialog, text="Add Randomly", command=add_smart_orbit_satellite_dummy)
    randomAdd.grid(row=5, columnspan=2)

    # Wait for the dialog to be destroyed
    root.wait_window(dialog)

    # Check if the dialog was submitted
    if 'name' in globals():
        # Create the satellite with the user's input
        satellite = SmartOrbitSatellite(name, semi_major_axis, eccentricity, inclination)
        satellites.append(satellite)

# Create a button to add a Smart Orbit Satellite
smart_button = Button(
    text="Manually Add Satellite",
    color=color.gray,
    position=(-0.7, 0.38),
    scale=(0.35, 0.05),
    text_size=5,
    on_click=add_smart_orbit_satellite_manual,
)

# Create buttons to control time factor
time_factors = [1, 5, 10, 100, 1000, 10000, 25000, 50000, 100000]
current_time_factor_index = len(time_factors) // 2  # Start with a medium time factor

time_factor_text = Text(
    text=f"Time Factor: {time_factors[current_time_factor_index]}x",
    position=(0, -0.4),
    origin=(0, 0),
    scale=0.75,
)


def update_time_factor_text():
    global current_time_factor_index
    time_factor_text.text = f"Time Factor: {time_factors[current_time_factor_index]}x"


def speed_up_time():
    global current_time_factor_index
    if current_time_factor_index < len(time_factors) - 1:
        current_time_factor_index += 1
        update_time_factor_text()


def slow_down_time():
    global current_time_factor_index
    if current_time_factor_index > 0:
        current_time_factor_index -= 1
        update_time_factor_text()


slow_down_button = Button(
    text="slow",
    color=color.gray,
    position=(-0.05, -0.45),
    scale=(0.07, 0.05),
    text_size=5,
    on_click=slow_down_time,
)

speed_up_button = Button(
    text="fast",
    color=color.gray,
    position=(0.05, -0.45),
    scale=(0.07, 0.05),
    text_size=5,
    on_click=speed_up_time,
)

camera_min_distance = 3
camera_max_distance = sky.scale_x - 1


def update():
    global satellites

    # Rotate the Earth and update satellites...
    earth.rotation_y -= (
        time.dt * time_factors[current_time_factor_index] * 360 / 86400
    )  # 360 degrees in 24 hours


app.run()
