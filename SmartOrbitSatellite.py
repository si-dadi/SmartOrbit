from ursina import *
import math
import random
import numpy as np
from PIL import Image, ImageDraw

G = 6.67430e-11  # Gravitational constant (m^3/kg/s^2)
earth_mass = 5.972e24  # Earth's mass (kg)
earth_radius = 1e10  # Earth's radius (m)

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
        self.semi_minor_axis = semi_major_axis * math.sqrt(1 - eccentricity**2)

        # Initialize the true anomaly (angle from closest approach)
        self.true_anomaly = random.uniform(0, 360)

        # Set initial position on surface of Earth in direction of semi-major axis
        self.position = (semi_major_axis, 0, 0)

        # Create an entity to represent the orbit
        self.orbit_entity = Entity(model=Circle(), scale=(semi_major_axis*2, self.semi_minor_axis*2), color=color.azure.tint(-0.5), double_sided=True)
        
    def update(self):
        # Update true anomaly based on Kepler's laws
        mean_motion = math.sqrt(G * earth_mass / self.semi_major_axis**3) * time.dt * self.time_factor
        mean_anomaly = mean_motion
        eccentric_anomaly = mean_anomaly + self.eccentricity * math.sin(mean_anomaly) * (1.0 + self.eccentricity * math.cos(mean_anomaly))
        self.true_anomaly = math.acos((math.cos(eccentric_anomaly) - self.eccentricity) / (1 - self.eccentricity * math.cos(eccentric_anomaly)))

        # Calculate position in orbital plane
        r = self.semi_major_axis * (1 - self.eccentricity**2) / (1 + self.eccentricity * math.cos(self.true_anomaly))
        x_orbit_plane = r * math.cos(self.true_anomaly)
        y_orbit_plane = r * math.sin(self.true_anomaly)

        # Rotate position to take into account inclination
        x = x_orbit_plane
        y = y_orbit_plane * math.sin(self.inclination)
        z = y_orbit_plane * math.cos(self.inclination)

        # Update position relative to global coordinates or Earth entity
        self.global_position = (x, y, z)

        # Update the position of the orbit entity to match the satellite's position
        self.orbit_entity.position = self.position
