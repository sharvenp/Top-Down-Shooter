
from settings import Settings

import math
import random

class Utils:

    @staticmethod
    def direction_position(position, angle, multiplier):
        h = math.cos(math.radians(abs(angle))) * multiplier
        v = math.sin(math.radians(abs(angle))) * multiplier
        x, y = position
        nx = round(x + h)
        ny = round(y + v)

        return (nx, ny)

    @staticmethod
    def get_look_angle(position, target):

        x, y = position
        px, py = target
        angle = round(math.degrees(math.atan2(py - y, px - x)))

        return angle

    @staticmethod
    def get_look_vector(angle):
        h = math.cos(math.radians(abs(angle)))
        v = math.sin(math.radians(abs(angle)))
        
        return (h, v)

    @staticmethod
    def normalize_vector(vector):
        x, y = vector
        magnitude = (x**2) + (y**2)

        return (x/magnitude, y/magnitude)

    @staticmethod
    def get_magnitude(vector):
        x, y = vector
        magnitude = (x**2) + (y**2)

        return magnitude

    @staticmethod
    def dot_product(v, u):
        vx, vy = v
        ux, uy = u

        prod = (vx * ux) + (vy * uy)

        return prod

    @staticmethod
    def get_vector_angle(v, u):

        dot = Utils.dot_product(v, u)
        magnitude = Utils.get_magnitude(v) * Utils.get_magnitude(u)

        a = dot / magnitude

        return math.acos(a) 

    @staticmethod
    def get_distance(p1, p2):
        x1, y1 = p1
        x2, y2 = p2

        a = (x2 - x1)**2
        b = (y2 - y1)**2

        return math.sqrt(a + b)

    @staticmethod
    def on_circle_point(center, radius):
        cx, cy = center
        angle = random.randint(0, 360)
        x = cx + round(math.cos(math.radians(angle)) * radius)
        y = cy + round(math.sin(math.radians(angle)) * radius)

        return (x, y)
