class dummySatellite:
    def __init__(self, name, inclination, semi_major_axis, semi_minor_axis, eccentricity):
        self.name = name  # Name of the satellite
        self.inclination = inclination  # Inclination angle in degrees
        self.semi_major_axis = semi_major_axis  # Semi-major axis in kilometers
        self.semi_minor_axis = semi_minor_axis  # Semi-minor axis in kilometers
        self.eccentricity = eccentricity  # Eccentricity of the orbit