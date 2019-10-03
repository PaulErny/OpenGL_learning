import pygame
import time
import OpenGL
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from vector import *
import numpy
import math


class FreeCam:
    def __init__(self):
        self.position = [0, 0, 5]
        self.direction = [0, 0, 0]
        self.right = [0, 0, 0]
        self.up = [0, 0, 0]
        self.horizontalAngle = 3.14
        self.verticalAngle = 0.00
        self.speed = 30.00
        self.mouseSpeed = 0.005
        self.keys = {'left': False,
                     'right': False,
                     'up': False,
                     'down': False}

    def compute_move(self, last_time):
        mouse_pos = pygame.mouse.get_pos()
        #pygame.mouse.set_pos(400, 300)

        self.horizontalAngle += self.mouseSpeed * float(800 / 2 - mouse_pos[0])
        self.verticalAngle += self.mouseSpeed * float(600 / 2 - mouse_pos[1])

        self.direction = [math.cos(self.verticalAngle) * math.sin(self.horizontalAngle),
                         math.sin(self.verticalAngle),
                         math.cos(self.verticalAngle) * math.cos(self.horizontalAngle)]

        self.right = [math.sin(self.horizontalAngle - float(3.14/2.0)),
                      0,
                      math.cos(self.horizontalAngle - float(3.14/2.0))]
        self.up = numpy.cross(self.right, self.direction)
        current_time = time.time()
        delta_time = float(current_time - last_time)

        if self.keys['left']:
            self.right = numpy.multiply(self.right, delta_time)
            self.right = numpy.multiply(self.right, self.speed)
            self.position = numpy.subtract(self.position, self.right)
        if self.keys['right']:
            self.right = numpy.multiply(self.right, delta_time)
            self.right = numpy.multiply(self.right, self.speed)
            self.position = numpy.add(self.position, self.right)
        if self.keys['up']:
            self.direction = numpy.multiply(self.direction, delta_time)
            self.direction = numpy.multiply(self.direction, self.speed)
            self.position = numpy.add(self.position, self.direction)
        if self.keys['down']:
            self.direction = numpy.multiply(self.direction, delta_time)
            self.direction = numpy.multiply(self.direction, self.speed)
            self.position = numpy.subtract(self.position, self.direction)

    def look(self):
        lookat = numpy.add(self.position, self.direction)
        gluLookAt(self.position[0], self.position[1], self.position[2],
                  lookat[0], lookat[1], lookat[2],
                  self.up[0], self.up[1], self.up[2])
        self.horizontalAngle = 3.14
        self.verticalAngle = 0.00
