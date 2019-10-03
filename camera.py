import pygame
import OpenGL
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

class camera:

    MOUSE_POS = (0, 0)
    PREV_MOUSE_POS = (0, 0)
    MOUSE_HELD_DOWN = False
    KEY_ENTER_PRESSED = False

    def __init__(self):
        self._motionSensitivity = 0.3
        self._scrollSensitivity = 1
        self._scrollUp = False
        self._scrollDown = False
        self.dst = 3
        self._angleY = 0
        self._angleZ = 0

    def look(self):
        gluLookAt(self.dst, 0, 0, 0, 0, 0, 0, 0, 1)
        glRotated(self._angleY, 0, 1, 0)
        glRotated(self._angleZ, 0, 0, 1)

    def onMouseMotion(self):
        if pygame.mouse.get_pressed()[0] == 1:
            if not self.MOUSE_HELD_DOWN:
                self.MOUSE_HELD_DOWN = True
                self.MOUSE_POS = pygame.mouse.get_pos()
                self.PREV_MOUSE_POS = self.MOUSE_POS
                xdiff = 0
                ydiff = 0
            else:
                self.MOUSE_POS = pygame.mouse.get_pos()
                xdiff = self.MOUSE_POS[0] - self.PREV_MOUSE_POS[0]
                ydiff = self.MOUSE_POS[1] - self.PREV_MOUSE_POS[1]
                self.PREV_MOUSE_POS = self.MOUSE_POS
            self._angleZ += xdiff * self._motionSensitivity
            self._angleY += ydiff * self._motionSensitivity
        else:
            self.MOUSE_POS = (0, 0)
            self.PREV_MOUSE_POS = (0, 0)
            self.MOUSE_HELD_DOWN = False

    def onScroll(self, button):
        if button == 4:
            self.dst += 0.2
        elif button == 5:
            self.dst -= 0.2
        if self.dst < 1.1:
            self.dst = 1.1

    def onKeyboard(self):
        keys = pygame.key.get_pressed()
        if keys[K_RETURN] and not self.KEY_ENTER_PRESSED:
            self.KEY_ENTER_PRESSED = True
            self._dst = 5
            self._angleY = 0
            self._angleZ = 0
        elif not keys[K_RETURN]:
            self.KEY_ENTER_PRESSED = False
        #if keys[K_RETURN] and not self.KEY_ENTER_PRESSED:
        #    self.KEY_ENTER_PRESSED = True
        #    self._dst += 0.5
        #    print(self._dst)
        #    gluLookAt(self._dst, 0, 0, 0, 0, 0, 0, 0, 1)

    # def setMotionSensitivity(self):

    # def setScrollSensitivity(self):
