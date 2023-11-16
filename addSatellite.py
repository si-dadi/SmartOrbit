from ursina import *
from ursina import destroy
from ursina.shaders import lit_with_shadows_shader
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton

from poliastro.bodies import Earth
from poliastro.twobody import Orbit
from poliastro.maneuver import Maneuver

from astropy import units as u

import random
import tkinter as tk
from world import *
from timeControl import *
from timeControl import getTimeFactor
from collisionAlerts import *
import math
import time

import numpy as np

satellites = []  # List of all satellites, *** to be used in ACAS prediction


class SmartOrbitSatellite(Entity):
    def __init__(
        self,
        name,
        semi_major_axis,
        semi_minor_axis,
        inclination,
        raan,
        argp,
        fuel_left,
        priority,
        collision_threshold,
    ):
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
        self.collision_threshold = collision_threshold

        eccentricity = math.sqrt(
            1
            - (
                (semi_minor_axis * semi_minor_axis)
                / (semi_major_axis * semi_major_axis)
            )
        )
        self.eccentricity = eccentricity
        self.orbit = Orbit.from_classical(
            Earth,
            semi_major_axis * u.km,
            eccentricity * u.one,
            inclination * u.deg,
            raan * u.deg,
            argp * u.deg,
            0 * u.deg,
        )

    def __str__(self):
        return f"SmartOrbitSatellite(name='{self.name}', semi_major_axis={self.semi_major_axis}, semi_minor_axis={self.semi_minor_axis}, inclination={self.inclination}, raan={self.raan}, argp={self.argp}, fuel_left={self.fuel_left}, priority={self.priority}, collision_threshold={self.collision_threshold}, position={self.position})"

    def destroySatelliteEntity(self):
        self.enabled = False  # Disabling the entity to hide it
        # if self in satellites:
        satellites.remove(self)
        destroy(self)
        self.color = (
            color.black
        )  # TODO: Find a proper way to delete this entity from scene!

    def update(self):
        dt_factor = getTimeFactor() / 1e5
        dt = time.dt * dt_factor
        self.orbit = self.orbit.propagate(dt * u.s)
        r = self.orbit.r.to(u.km).value / earth.scale_x
        self.position = (
            r[0] * earth.scale_x,
            r[1] * earth.scale_y,
            r[2] * earth.scale_z,
        )
        # print(self.position)


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
    collision_threshold_label = tk.Label(
        dialog, text="Collision Threshold Distance (bw [0, 0.1]):"
    )
    collision_threshold_entry = tk.Entry(dialog)

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
    collision_threshold_label.grid(row=8, column=0)
    collision_threshold_entry.grid(row=8, column=1)

    def submit():
        global name, semi_major_axis, semi_minor_axis, inclination, raan, argp, fuel_left, priority, collision_threshold
        name = name_entry.get()
        semi_major_axis = float(semi_major_axis_entry.get())
        semi_minor_axis = float(semi_minor_axis_entry.get())
        inclination = float(inclination_entry.get())
        raan = float(raan_entry.get())
        argp = float(argp_entry.get())
        fuel_left = float(fuel_left_entry.get())
        priority = int(priority_entry.get())
        collision_threshold = float(collision_threshold_entry.get())

        satellite = SmartOrbitSatellite(
            name,
            semi_major_axis,
            semi_minor_axis,
            inclination,
            raan,
            argp,
            fuel_left,
            priority,
            collision_threshold,
        )
        satellite.parent = universalReferencepoint
        satellites.append(satellite)
        print("Satellite data: ", satellites)

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
        collision_threshold = random.uniform(0, 0.1)

        satellite = SmartOrbitSatellite(
            name,
            semi_major_axis,
            semi_minor_axis,
            inclination,
            raan,
            argp,
            fuel_left,
            priority,
            collision_threshold,
        )
        satellite.parent = universalReferencepoint
        satellites.append(satellite)
        # print("Satellite data: ", satellites)

        dialog.destroy()
        update_camera_follow_buttons()

    submit_button = tk.Button(dialog, text="Submit", command=submit)
    submit_button.grid(row=9, column=0, columnspan=2)
    or_label = tk.Label(dialog, text="OR")
    or_label.grid(row=10, column=0, columnspan=2)
    randomAdd = tk.Button(
        dialog, text="Add Randomly", command=add_smart_orbit_satellite_dummy
    )
    randomAdd.grid(row=11, column=0, columnspan=2)

    root.wait_window(dialog)

    if "name" in globals():
        satellite = SmartOrbitSatellite(
            name,
            semi_major_axis,
            semi_minor_axis,
            inclination,
            raan,
            argp,
            fuel_left,
            priority,
            collision_threshold,
        )
        satellite.parent = universalReferencepoint
        # print("Satellite data: ", satellites)
        update_camera_follow_buttons()  # Call the update function here

add_satellite_button = Button(
    text="Add Satellite",
    color=color.gray,
    position=(-0.7, 0.4),
    scale=(0.35, 0.05),
    text_size=5,
    on_click=add_smart_orbit_satellite_manual,
)

cameraShifted = False
following_satellite = None  # Add a variable to track the satellite being followed

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
                position=(
                    -0.7,
                    (0.2 - 0.06 * (i + 1)),
                ),  # Offset from "Reset Camera" button
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
    else:
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


def getSatellites():
    return satellites


def calculate_euclidean_distance(vec1, vec2):
    dx = vec1[0] - vec2[0]
    dy = vec1[1] - vec2[1]
    dz = vec1[2] - vec2[2]
    return math.sqrt(dx * dx + dy * dy + dz * dz)

def predict_collision():
    satellitesSnapshot = getSatellites()

    if satellitesSnapshot.__len__() > 1:

        for satellite in satellitesSnapshot:
            for moreSatellite in satellitesSnapshot:
                if satellite == moreSatellite:
                    continue
                distance = calculate_euclidean_distance(
                    moreSatellite.position, satellite.position
                )
                if distance <= max(
                    moreSatellite.collision_threshold, satellite.collision_threshold
                ):
                    collision_alerts.append(
                        "Collision occured between "
                        + moreSatellite.name
                        + " and "
                        + satellite.name
                        + "!"
                    )
                    satellite.destroySatelliteEntity()
                    moreSatellite.destroySatelliteEntity()

slider_value = 1
def getSliderValue():
    slider_value = int(time_range_slider.value)
    return slider_value

future_times = [t for t in range(1, slider_value, 1)]

def getFutureTimes():
    slider_value = getSliderValue()
    future_times = [t for t in range(1, slider_value + 1, 1)]
    return future_times
# Set initial visibility to False
slider_visible = False
button_visible = False
slider_text_visible = False
sliderText = Text(
    text="Select Prediction Time (in hrs)", position=(0.5, 0.45), text_size=5, scale=0.75, visible=slider_text_visible
)

time_range_slider = Slider(
    dynamic=True,
    min=1,
    max=24,
    default=1,
    step=1,
    x=0.5,
    y=0.4,
    bar_color=color.gray,
    scale=0.5,
    on_value_changed=getSliderValue,
    visible=slider_visible,
)

collision_button = Button(
    text="Predict Collisions",
    color=color.gray,
    position=(0.65, 0.35),
    scale=(0.35, 0.05),
    text_size=5,
    on_click=lambda: predict_future_collisions(future_times),
    visible=button_visible,
)
def update_visibility():
    global slider_visible, button_visible, slider_text_visible
    satellites_snapshot = getSatellites()

    # Check if there are at least 2 satellites in the scene
    if satellites_snapshot.__len__() > 1:
        slider_visible = True
        button_visible = True
        slider_text_visible = True
    else:
        slider_visible = False
        button_visible = False
        slider_text_visible = False

    time_range_slider.visible = slider_visible
    collision_button.visible = button_visible
    sliderText.visible = slider_text_visible
def predict_future_collisions(future_times):
    satellitesSnapshot = getSatellites()
    future_times = getFutureTimes()
    # print("Called Me?...", slider_value, (future_times))
    if satellitesSnapshot.__len__() > 1:
        start_time = time.perf_counter()

        for satellite in satellitesSnapshot:
            satellite.orbit = Orbit.from_vectors(
                Earth, satellite.orbit.r, satellite.orbit.v
            )

        # Initialize a flag to track whether a collision has been detected
        collision_detected = False

        for satellite in satellitesSnapshot:
            if collision_detected:
                break  # Exit the loop if collision has already been detected
            for moreSatellite in satellitesSnapshot:
                if satellite == moreSatellite:
                    continue

                future_positions_satellite = [
                    satellite.orbit.propagate((1 / 86400) * time * u.s)
                    for time in future_times
                ]
                future_positions_moreSatellite = [
                    moreSatellite.orbit.propagate((1 / 86400) * time * u.s)
                    for time in future_times
                ]

                for idx, (pos1, pos2) in enumerate(
                    zip(future_positions_satellite, future_positions_moreSatellite)
                ):
                    relative_distance = calculate_euclidean_distance(
                        (pos1.r / u.km), (pos2.r / u.km)
                    )

                    if relative_distance <= max(
                        moreSatellite.collision_threshold,
                        satellite.collision_threshold,
                    ):
                        collision_time = future_times[idx]
                        collision_alerts.append(
                            f"Collision predicted between {moreSatellite.name} and {satellite.name} "
                            f"in {collision_time / 3600:.3f} hours!"
                        )
                        collision_detected = True
                        break  # Exit the loop if a collision is detected

        end_time = time.perf_counter()
        print("Time taken: {:.6f} microseconds".format((end_time - start_time) * 1e6))

def lambert_transfer(satellite):
    # Get the current epoch of the satellite's orbit
    current_epoch = satellite.orbit.epoch
    # Create a new orbit with modified parameters
    modifications = Orbit.from_classical(
        Earth,
        satellite.semi_major_axis * 2 * u.km,
        satellite.eccentricity * u.one,
        satellite.inclination * u.deg,
        satellite.raan * u.deg,
        satellite.argp * u.deg,
        0 * u.deg,
    )

    modifications.epoch.isot = current_epoch.isot

    # try:
    #     maneuver = Maneuver.lambert(satellite.orbit, modifications)
    #     transfer_orbit, new_orbit = satellite.orbit.apply_maneuver(maneuver, intermediate=True)
    #     print(maneuver, transfer_orbit, new_orbit)
    # except AssertionError as e:
    #     print(f"Error: {e}")
    #     print(f"Current orbit: {satellite.orbit}")
    #     print(f"New orbit: {modifications}")
    #     return


def test_fn():
    if satellites:
        lambert_transfer(satellites[0])
        print(satellites[0].orbit)

test_btn = Button(
    text="Fuck Orbit",
    color=color.gray,
    scale=(0.1, 0.05),
    position=(-0.65, -0.35),
    on_click=test_fn,
)


def update():
    if cameraShifted and following_satellite:
        target_position = 2 * following_satellite.position
        camera.position = lerp(camera.position, target_position, 0.19)
        # camera.look_at(earth)   # TODO: Fix this

    earth.rotation_y -= time.dt * getTimeFactor() * 360 / 86400

    update_alerts()
    predict_collision()# Continuously monitor for collisions and destroy satellites if collision occurs
    update_visibility()
