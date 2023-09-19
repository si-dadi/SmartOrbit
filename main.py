from SmartOrbitSatellite import SmartOrbitSatellite
from ursina import *
import math
import random

app = Ursina()

window.title = 'SafeOrbit'
window.borderless = False
window.exit_button.visible = False
window.fps_counter.enabled = True

camera = EditorCamera(rotation_speed=100, pan_speed=(0.5, 0.5), zoom_speed=1, position=(0, 0, 0), target=(0, 0, 0))

earth_texture = load_texture("textures/wallpaperflare.com_wallpaper (2).jpg")
earth = Entity(
    model="sphere",
    texture=earth_texture,
    scale=2,
    subdivisions=256,  # Increase subdivisions for smoother appearance
    position=(0, 0, 0),
)

sun_light = DirectionalLight(color=color.white, y=2, z=-3, shadows=True)
sun_light.rotation = (10, 30, 30)

sky_texture = load_texture("textures/black-color-solid-background-1920x1080.png")
sky = Entity(model="sphere", texture=sky_texture, scale=1000, double_sided=True)
sky.shader = 'unlit'

# Constants
G = 6.67430e-11  # Gravitational constant (m^3/kg/s^2)
earth_mass = 5.972e24  # Earth's mass (kg)

# Initial conditions
satellites = []
orbital_positions = []

def add_smart_orbit_satellite():
    name = f"Satellite{len(satellites) + 1}"
    semi_major_axis = random.uniform(2, 20)
    semi_minor_axis = random.uniform(2, semi_major_axis - 1)
    eccentricity = math.sqrt(1 - (semi_minor_axis ** 2 / semi_major_axis ** 2))
    inclination = random.uniform(0, 180)
    satellite = SmartOrbitSatellite(name, semi_major_axis, semi_minor_axis, eccentricity, inclination, time_factors[current_time_factor_index])
    satellites.append(satellite)
    satellite.parent = earth  # Add the satellite as a child of the Earth entity
    print(f"Smart satellite '{name}' added!")

# Create buttons
Button(text='Add Dummy Satellite', color=color.gray, position=(-0.7, 0.45), scale=(0.35, 0.05), text_size=5)

# Create a button to add a Smart Orbit Satellite
smart_button = Button(
    text='Add Smart Orbit Satellite',
    color=color.gray,
    position=(-0.7, 0.38),
    scale=(0.35, 0.05),
    text_size=5,
    on_click=add_smart_orbit_satellite
)

# Create a list to store orbital trail positions
orbital_positions = []

# Create buttons to control time factor
time_factors = [1, 5, 10, 100, 1000, 5000, 10000, 20000]
current_time_factor_index = 5  # Index of the current time factor

time_factor_text = Text(text=f'Time Factor: {time_factors[current_time_factor_index]}x', position=(0, -0.4),
                        origin=(0, 0), scale=0.75)

def update_time_factor_text():
    global current_time_factor_index
    time_factor_text.text = f'Time Factor: {time_factors[current_time_factor_index]}x'

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
    text='slow',
    color=color.gray,
    position=(-0.05, -0.45),
    scale=(0.07, 0.05),
    text_size=5,
    on_click=slow_down_time
)

speed_up_button = Button(
    text='fast',
    color=color.gray,
    position=(0.05, -0.45),
    scale=(0.07, 0.05),
    text_size=5,
    on_click=speed_up_time
)

camera_min_distance = 3
camera_max_distance = sky.scale_x - 1  # You already have this defined

def update():
    global satellites, orbital_positions

    # Rotate the Earth
    earth.rotation_y -= time.dt * time_factors[current_time_factor_index] * 360 / 86400  # 360 degrees in 24 hours

app.run()
