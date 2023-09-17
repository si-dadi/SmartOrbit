class SmartOrbitSatellite:
    def __init__(self, name, inclination, semi_major_axis, semi_minor_axis, eccentricity):
        self.name = name
        self.inclination = inclination
        self.semi_major_axis = semi_major_axis
        self.semi_minor_axis = semi_minor_axis
        self.eccentricity = eccentricity
        self.orbit_angle = 0  # Initial angle

    def set_position(self, angle):
        self.orbit_angle = angle

    def update_position(self, delta_angle):
        self.orbit_angle += delta_angle
