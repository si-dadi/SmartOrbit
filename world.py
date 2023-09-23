from ursina import *

app = Ursina()

window.title = "SafeOrbit"
window.borderless = False
window.exit_button.visible = False
window.fps_counter.enabled = True

sun_light1 = DirectionalLight(color=color.white, y=60, z=-90, shadows=True, range=100)
sun_light1.rotation = (10, 30, 30)
sun_light2 = DirectionalLight(color=color.white, y=60, z=-90, shadows=True, range=100)
sun_light2.rotation = (10, 30, 30)
sun_light3 = DirectionalLight(color=color.white, y=60, z=-90, shadows=True, range=100)
sun_light3.rotation = (10, 30, 30)
sun_light = DirectionalLight(color=color.yellow, y=60, z=-90, shadows=True, range=100)
sun_light.rotation = (10, 30, 30)

earth = Entity(model="models/EarthClouds_1_12756.glb", scale=0.002, position=(0, 0, 0), render_queue=1)

universalReferencepoint = Entity(
    model="sphere", x=0, y=0, z=0, scale=1.9, color=color.black
)
sky_texture = load_texture("textures/black-color-solid-background-1920x1080.png")
sky = Entity(model="sphere", texture=sky_texture, scale=1000, double_sided=True)
sky.shader = "unlit"

camera = EditorCamera(
    rotation_speed=100,
    pan_speed=(0.5, 0.5),
    zoom_speed=1,
    position=(0, 0, 0),
    target=(0, 0, 0),
)

camera_min_distance = 3
camera_max_distance = sky.scale_x - 1

time_factors = [1, 5, 10, 100, 1000, 10000, 25000, 50000, 100000, 250000, 500000, 1000000]
current_time_factor_index = 5