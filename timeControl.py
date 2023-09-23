from ursina import *
from world import *
from world import current_time_factor_index, time_factors

def getTimeFactor():
    return time_factors[current_time_factor_index]

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

time_factor_text = Text(
    text=f"Time Factor: {time_factors[current_time_factor_index]}x",
    position=(0, -0.4),
    origin=(0, 0),
    scale=0.75,
)

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

def update():
    # Rotate the Earth and update satellites...
    earth.rotation_y -= (
        time.dt * time_factors[current_time_factor_index] * 360 / 86400
    )