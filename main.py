from ursina import *
from poliastro.bodies import Earth
from poliastro.twobody import Orbit
from astropy import units as u
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
    subdivisions=256,
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

class SmartOrbitSatellite(Entity):
    def __init__(self, name):
        super().__init__(
            model="models/uploads_files_1985975_star+wars.obj",  # Replace with your satellite model
            scale=(0.025, 0.025, 0.025),
        )
        self.name = name

        # Random orbital parameters
        semi_major_axis = random.uniform(2, 20) * u.km
        eccentricity = random.uniform(0, 1) * u.one
        inclination = random.uniform(0, 180) * u.deg

        # Create an orbit using poliastro
        self.orbit = Orbit.from_classical(Earth, semi_major_axis, eccentricity,
                                          inclination, 0 * u.deg, 0 * u.deg, 0 * u.deg)

    def update(self):
        # Propagate the orbit to the current time
        dt_factor=time_factors[current_time_factor_index] / 100  # time factor to speed up the simulation 
        dt=time.dt*dt_factor 
        self.orbit = self.orbit.propagate(dt * u.s)

        # Update the position of the satellite
        r = self.orbit.r.to(u.km).value / earth.scale_x   # Convert position to Earth radii
        self.position = (r[0], r[1], r[2])

def add_smart_orbit_satellite():
    name = f"Satellite{len(satellites) + 1}"
    satellite = SmartOrbitSatellite(name)
    satellites.append(satellite)
    satellite.parent = earth   # Add the satellite as a child of the Earth entity
    print(f"Smart satellite '{name}' added!")

# Create buttons and other UI elements...
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

# Create buttons to control time factor
time_factors = [1, 5, 10, 100, 1000, 10000, 25000, 50000, 100000]
current_time_factor_index = len(time_factors) // 2   # Start with a medium time factor

time_factor_text = Text(text=f'Time Factor: {time_factors[current_time_factor_index]}x', position=(0,-0.4),
                        origin=(0, 0), scale=2)

def update_time_factor_text():
    global current_time_factor_index
    time_factor_text.text=f'Time Factor: {time_factors[current_time_factor_index]}x'

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

slow_down_button=Button(
    text='slow',
    color=color.gray,
    position=(-0.05, -0.45),
    scale=(0.07, 0.05),
    text_size=5,
    on_click=slow_down_time
)

speed_up_button=Button(
    text='fast',
    color=color.gray,
    position=(0.05, -0.45),
    scale=(0.07, 0.05),
    text_size=5,
    on_click=speed_up_time
)

camera_min_distance = 3
camera_max_distance = sky.scale_x - 1

def update():
    global satellites

    # Rotate the Earth and update satellites...
    earth.rotation_y -= time.dt * time_factors[current_time_factor_index] * 360 / 86400  # 360 degrees in 24 hours

app.run()
