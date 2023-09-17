from ursina import *
import math
from SmartOrbitSatellite import SmartOrbitSatellite  # Import the SmartOrbitSatellite class

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
# orbit_radius = 3  # Radius of the circular orbit
orbit_speed = 360 / 15  # Degrees per second to complete one orbit in 15 seconds
orbit_angle = 0  # Initialize orbit angle

camera_min_distance = 3
camera_max_distance = sky.scale_x - 1


def add_smart_orbit_satellite():
    global satellites, satellite_entity, orbital_positions

    # Create a new SmartOrbitSatellite instance
    new_satellite = SmartOrbitSatellite(
        name="Smart Satellite",
        inclination=0.0,  # Set inclination angle to 0 for a flat orbit
        semi_major_axis=8.0,  # Set semi-major axis for an elliptical orbit
        semi_minor_axis=4.0,  # Set semi-minor axis for an elliptical orbit (half of the major axis)
        eccentricity=0.0  # Eccentricity should be 0 for a circular orbit
    )

    # Append the satellite to the list
    satellites.append(new_satellite)

    # Calculate the initial position on the elliptical orbit
    satellite_angle = len(satellites) * (360 / len(satellites))  # Equally spaced angles
    new_satellite.set_position(satellite_angle)

    # Create an Ursina Entity for the satellite
    satellite_entity = Entity(
        model="models/uploads_files_1985975_star+wars.obj",  # Replace with your satellite model
        scale=(0.025, 0.025, 0.025),
        position=(new_satellite.semi_major_axis * math.cos(math.radians(satellite_angle)),
                  0,
                  new_satellite.semi_minor_axis * math.sin(math.radians(satellite_angle)))
    )

    # Clear the orbital trail
    orbital_positions = []

    print("Smart orbit satellite added!")


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

satellites = []
satellite_entity = None  # Initialize satellite_entity

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

def update():
    global satellite_entity, orbit_speed, orbit_angle

    # Rotate the Earth
    earth.rotation_y -= time.dt * time_factors[current_time_factor_index] * 360/86400  # 360 degrees in 24 hours

    if satellite_entity:
        # Calculate satellite position in elliptical orbit
        orbit_angle += orbit_speed * time.dt  # Adjust orbit speed based on time factor
        semi_major_axis = satellites[0].semi_major_axis  # Convert to meters
        semi_minor_axis = satellites[0].semi_minor_axis   # Convert to meters
        distance_from_earth = math.sqrt(
            (semi_major_axis * math.cos(math.radians(orbit_angle))) ** 2 + (semi_minor_axis * math.sin(
                math.radians(orbit_angle))) ** 2)

        # Calculate orbital speed based on current distance from Earth
        gravitational_constant = 6.674 * (10 ** -11)  # Gravitational constant in m^3/kg/s^2
        earth_mass = 5.972 * (10 ** 24)  # Earth's mass in kg
        orbital_speed = math.sqrt((gravitational_constant * earth_mass) / distance_from_earth)

        # Update satellite position
        satellite_x = semi_major_axis * math.cos(math.radians(orbit_angle))
        satellite_z = semi_minor_axis * math.sin(math.radians(orbit_angle))
        satellite_entity.position = (satellite_x, 0, satellite_z)

        # Add the current satellite position to the orbital trail
        orbital_positions.append(satellite_entity.position)

        # Remove old positions to limit the trail length
        if len(orbital_positions) > 100:
            orbital_positions.pop(0)

        # Create a Line entity to represent the orbital trail
        # orbital_line = Line(positions=orbital_positions, color=color.gray, thickness=0.01)

        # Adjust camera distance based on satellite position
        camera_distance = distance(camera.position, (0, 0, 0))
        if camera_distance < camera_min_distance:
            camera.position += (camera.position.normalized() * camera_min_distance - camera.position) * time.dt * 2
        elif camera_distance > camera_max_distance:
            camera.position += (camera.position.normalized() * camera_max_distance - camera.position) * time.dt * 2

app.run()
