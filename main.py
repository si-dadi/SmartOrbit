from ursina import *
import math
from SmartOrbitSatellite import SmartOrbitSatellite  # Import the SmartOrbitSatellite class

app = Ursina()

window.title = 'SafeOrbit'                
window.borderless = False               
window.exit_button.visible = False      
# window.entities.visible = False      
# window.exit_button.visible = False      
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

sky_texture = load_texture("textures/abstract-geometric-background-shapes-texture.jpg")
sky = Entity(model="sphere", texture=sky_texture, scale=1000, double_sided=True)
sky.shader = 'unlit'

# Constants
orbit_radius = 3  # Radius of the circular orbit
orbit_speed = 360 / 15  # Degrees per second to complete one orbit in 15 seconds
orbit_angle = 0

camera_min_distance = 3
camera_max_distance = sky.scale_x - 1

# Create buttons
Button(text='Add Dummy Satellite', color=color.gray, position=(-0.7,0.45), scale=(0.35,0.05), text_size=5)

satellites = []
satellite_entity = None  # Initialize satellite_entity

def add_smart_orbit_satellite():
    global satellites, satellite_entity

    # Create a new SmartOrbitSatellite instance
    new_satellite = SmartOrbitSatellite(
        name="Smart Satellite",
        inclination=45.0,            # Set inclination angle
        semi_major_axis=3.4,        # Set semi-major axis
        semi_minor_axis=2.9,        # Set semi-minor axis
        eccentricity=0.1            # Set eccentricity
    )
    
    # Append the satellite to the list
    satellites.append(new_satellite)

    # Calculate the initial position on the circular orbit
    satellite_angle = len(satellites) * (360 / len(satellites))  # Equally spaced angles
    new_satellite.set_position(satellite_angle)

    # Create an Ursina Entity for the satellite
    satellite_entity = Entity(
        model="models/uploads_files_1985975_star+wars.obj",  # Replace with your satellite model
        scale=(0.025, 0.025, 0.025),
        position=(new_satellite.semi_major_axis * math.cos(math.radians(satellite_angle)), 0, new_satellite.semi_minor_axis * math.sin(math.radians(satellite_angle)))
    )

    print("Smart orbit satellite added!")

smart_button = Button(
    text='Add Smart Orbit Satellite',
    color=color.gray,
    position=(-0.7, 0.38),
    scale=(0.35, 0.05),
    text_size=5,
    on_click=add_smart_orbit_satellite  # Call the function on click
)

def update():
    global orbit_angle, satellite_entity

    # Rotate the Earth
    earth.rotation_y -= time.dt * 360/30  # Rotate Earth once every 30 seconds
    # Calculate satellite position in circular orbit
    orbit_angle += orbit_speed * time.dt
    satellite_x = orbit_radius * math.cos(math.radians(orbit_angle))
    satellite_z = orbit_radius * math.sin(math.radians(orbit_angle))

    # Update satellite position
    if satellite_entity:
        satellite_entity.position = (satellite_x, 0, satellite_z)

    # Adjust camera distance based on satellite position
    camera_distance = distance(camera.position, (0, 0, 0))
    if camera_distance < camera_min_distance:
        camera.position += (camera.position.normalized() * camera_min_distance - camera.position) * time.dt*2
    elif camera_distance > camera_max_distance:
        camera.position += (camera.position.normalized() * camera_max_distance - camera.position) * time.dt*2

app.run()
