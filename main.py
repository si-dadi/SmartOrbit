from ursina import *
import math
import random
# from SmartOrbitSatellite import SmartOrbitSatellite

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

class SmartOrbitSatellite(Entity):
    def __init__(self, name, semi_major_axis, eccentricity, inclination, time_factor):
        super().__init__(
            model="models/uploads_files_1985975_star+wars.obj",  # Replace with your satellite model
            scale=(0.025, 0.025, 0.025),
        )
        self.name = name
        self.semi_major_axis = semi_major_axis
        self.eccentricity = eccentricity
        self.inclination = math.radians(inclination)  # Convert inclination to radians
        self.time_factor = time_factor  # Store the time factor

        # Calculate the semi-minor axis based on the eccentricity and semi-major axis
        self.semi_minor_axis = self.semi_major_axis * math.sqrt(1 - self.eccentricity**2)

        # Initialize the true anomaly (angle from closest approach)
        self.true_anomaly = random.uniform(0, 360)

        # Set initial position on surface of Earth in direction of semi-major axis
        r = self.semi_major_axis * (1 - self.eccentricity**2) / (1 + self.eccentricity * math.cos(math.radians(self.true_anomaly)))
        x_orbit_plane = r * math.cos(math.radians(self.true_anomaly))
        y_orbit_plane = r * math.sin(math.radians(self.true_anomaly))
        x = x_orbit_plane
        y = y_orbit_plane * math.sin(self.inclination)
        z = y_orbit_plane * math.cos(self.inclination)
        self.position = (x, y, z)

        # Create an entity to represent the orbit
        self.orbit_entity = Entity(model=Cylinder(height=0.01), scale=(self.semi_major_axis*2, 1, self.semi_minor_axis*2), color=color.azure.tint(-0.5), double_sided=True)
        
    def update(self):
        # Update true anomaly based on Kepler's laws
        mean_motion = math.sqrt(G * earth_mass / (self.semi_major_axis**3)) * time.dt * self.time_factor
        mean_anomaly = mean_motion
        eccentric_anomaly = mean_anomaly + self.eccentricity * math.sin(mean_anomaly) * (1.0 + self.eccentricity * math.cos(mean_anomaly))
        self.true_anomaly += mean_motion

        # Calculate position in orbital plane
        r = self.semi_major_axis * (1 - self.eccentricity**2) / (1 + self.eccentricity * math.cos(math.radians(self.true_anomaly)))
        
        # Convert to spherical coordinates
        theta = math.radians(self.true_anomaly)
        phi = math.radians(90 - self.inclination)
        
        x = r * math.sin(phi) * math.cos(theta)
        y = r * math.sin(phi) * math.sin(theta)
        z = r * math.cos(phi)

        # Update position relative to global coordinates or Earth entity
        self.global_position = (x, y, z)

def add_smart_orbit_satellite():
    name = f"Satellite{len(satellites) + 1}"
    semi_major_axis = random.uniform(2, 20)
    eccentricity = random.uniform(0, 1)
    inclination = random.uniform(0, 180)
    satellite = SmartOrbitSatellite(name, semi_major_axis, eccentricity, inclination, time_factors[current_time_factor_index])
    satellites.append(satellite)
    satellite.parent = earth  # Add the satellite as a child of the Earth entity
    print(f"Smart satellite '{name}' added! (Semi-major axis: {semi_major_axis}, Eccentricity: {eccentricity}, Inclination: {inclination})")

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
camera_max_distance = sky.scale_x - 1

def update():
    global satellites

    # Rotate the Earth and update satellites...
    earth.rotation_y -= time.dt * time_factors[current_time_factor_index] * 360 / 86400  # 360 degrees in 24 hours

app.run()
