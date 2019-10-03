import pygame
from cube import *
import time
from camera import camera
from FreeCam import FreeCam
import OpenGL
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

fps = 0
elapsed = 0


def limitFps(maxFps, clock):
    global fps
    global elapsed
    elapsed += clock.tick(maxFps)
    fps += 1
    if elapsed >= 1000:
        elapsed = 0
        fps = 0


def main(maxFps = 50):

    # pygame init
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL | OPENGLBLIT)
    image = pygame.image.load("San.png").convert()
    pygame.display.set_caption("Text")
    pygame.display.set_icon(image)
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()

    # openGL init
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(80, 800 / 600, 0.1, 500)  # fov
    glEnable(GL_DEPTH_TEST)  # explicit
    cam = FreeCam()
    # main loop
    while True:
        start = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    cam.keys['left'] = True
                if event.key == pygame.K_RIGHT:
                    cam.keys['right'] = True
                if event.key == pygame.K_UP:
                    cam.keys['up'] = True
                if event.key == pygame.K_DOWN:
                    cam.keys['down'] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    cam.keys['left'] = False
                if event.key == pygame.K_RIGHT:
                    cam.keys['right'] = False
                if event.key == pygame.K_UP:
                    cam.keys['up'] = False
                if event.key == pygame.K_DOWN:
                    cam.keys['down'] = False

        cam.compute_move(start)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        cam.look()
        # draw static object
        #drawAxes()
        #drawFloor()
        drawFullCube()
        glFlush()

        pygame.display.flip()

        limitFps(maxFps, clock)


main()
