import math


class Vector(object):
    def __init__(self, x, y, z):
        """ Create a vector, example: v = Vector(1,2) """
        self.x = x
        self.y = y
        self.z = z

    def norm(self):
        """ Returns the norm (length, magnitude) of the vector """
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def normalize(self):
        """ Returns a normalized unit vector """
        norm = self.norm()
        return Vector(self.x / norm, self.y / norm, self.z / norm)

    def cross_product(self, other):
        t = Vector(0, 0, 0)
        t.x = self.y * other.z - self.z * other.y
        t.y = self.z * other.x - self.x * other.z
        t.z = self.x * other.y - self.y * other.x
        return t

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

    def __mul__(self, other):
        self.x *= other
        self.y *= other
        self.z *= other
        return self

    def __add__(self, other):
        t = self
        t += other
        return t