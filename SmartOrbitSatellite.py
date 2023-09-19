from ursina import *
import math
import random
import numpy as np
from PIL import Image, ImageDraw

G = 6.67430e-11  # Gravitational constant (m^3/kg/s^2)
earth_mass = 5.972e24  # Earth's mass (kg)

class SmartOrbitSatellite(Entity):
    def __init__(self, name, semi_major_axis, semi_minor_axis, eccentricity, inclination, time_factor):
        super().__init__(
            model="models/uploads_files_1985975_star+wars.obj",  # Replace with your satellite model
            scale=(0.025, 0.025, 0.025),
            # color=color.random_color(),
        )
        self.name = name
        self.semi_major_axis = semi_major_axis
        self.semi_minor_axis = semi_minor_axis
        self.eccentricity = eccentricity
        self.inclination = inclination
        self.orbit_angle = random.uniform(0, 360)  # Initial angle
        self.time_factor = time_factor  # Store the time factor
        self.orbital_speed = math.sqrt(G * earth_mass / (semi_major_axis * 1e20))
        
        # Create an ellipse to represent the satellite's orbit
        self.orbit_ellipse = Entity(
            model='quad',
            color=color.clear,  # Make the ellipse transparent
            scale=(semi_major_axis * 2, semi_minor_axis * 2, 1),  # Scale to create an ellipse
            parent=self,  # Make the ellipse a child of the satellite
        )

    def update(self):
        self.orbit_angle += self.orbital_speed * time.dt   # Use the stored time factor
        x = self.semi_major_axis * math.cos(math.radians(self.orbit_angle))
        z = self.semi_minor_axis * math.sin(math.radians(self.orbit_angle))
        self.position = (x, 0, z)
