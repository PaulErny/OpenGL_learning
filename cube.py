import pygame
import OpenGL
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )

edges = (
    (0,1,3),
    (6,0,3),
    (6,0,4),
    (2,1,3),
    (2,3,7),
    (4,1,0),
    (7,3,6),
    (5,6,7),
    (4,1,5),
    (5,1,2),
    (4,5,6),
    (5,7,2)
    )


def drawFullCube():
    glBegin(GL_QUADS)

    glColor3ub(255, 0, 0)  # face rouge
    glVertex3d(1, 1, 1)
    glVertex3d(1, 1, -1)
    glVertex3d(-1, 1, -1)
    glVertex3d(-1, 1, 1)

    glColor3ub(0, 255, 0)  # face verte
    glVertex3d(1, -1, 1)
    glVertex3d(1, -1, -1)
    glVertex3d(1, 1, -1)
    glVertex3d(1, 1, 1)

    glColor3ub(0, 0, 255)  # face bleue
    glVertex3d(-1, -1, 1)
    glVertex3d(-1, -1, -1)
    glVertex3d(1, -1, -1)
    glVertex3d(1, -1, 1)

    glColor3ub(255, 255, 0)  # face jaune
    glVertex3d(-1, 1, 1)
    glVertex3d(-1, 1, -1)
    glVertex3d(-1, -1, -1)
    glVertex3d(-1, -1, 1)

    glColor3ub(0, 255, 255)  # face cyan
    glVertex3d(1, 1, -1)
    glVertex3d(1, -1, -1)
    glVertex3d(-1, -1, -1)
    glVertex3d(-1, 1, -1)

    glColor3ub(255, 0, 255)  # face magenta
    glVertex3d(1, -1, 1)
    glVertex3d(1, 1, 1)
    glVertex3d(-1, 1, 1)
    glVertex3d(-1, -1, 1)

    glEnd()


def drawEdges():
    for edge in edges:
        glBegin(GL_LINE_LOOP)
        for vertex in edge:
            glVertex3fv(verticies[vertex])
        glEnd()


def drawVertices():
    glBegin(GL_POINT)

    glColor4f(0.5, 0.5, 0, 0.5)

    glVertex3d(1, -1, -1)
    glVertex3d(1, 1, -1)
    glVertex3d(-1, 1, -1)
    glVertex3d(-1, -1, -1)
    glVertex3d(1, -1, 1)
    glVertex3d(1, 1, 1)
    glVertex3d(-1, -1, 1)
    glVertex3d(-1, 1, 1)

    glEnd()


def drawAxes():
    glPushMatrix()
    glLoadIdentity()

    #glRotated(rotX, 1.0, 0.0, 0.0)
    #glRotated(rotY, 0.0, 1.0, 0.0)
    #glRotated(rotZ, 0.0, 0.0, 1.0)

    #glTranslatef(-3.0, -2.0, 0.0)

    glBegin(GL_LINES)
    # draw line for x axis
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(1.0, 0.0, 0.0)
    # draw line for y axis
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 1.0, 0.0)
    # draw line for Z axis
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 1.0)
    glEnd()

    glPopMatrix()


def drawFloor():
    glPushMatrix()
    glLoadIdentity()

    glBegin(GL_QUADS)
    glColor3f(0.8, 0.8, 0.8)
    glVertex3d(5.0, -1, 5.0)
    glVertex3d(-5.0, -1, 5.0)
    glVertex3d(-5.0, -1, -5.0)
    glVertex3d(5.0, -1, -5.0)
    glEnd()

    glPopMatrix()


def test_main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(70, 800 / 600, 0.1, 1000)
    glEnable(GL_DEPTH_TEST)
    glPointSize(5)

    gluLookAt(0, -5, 0, 0, 0, 0, 0, 0, 1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        # clean and display rotating cube

        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # glMatrixMode(GL_MODELVIEW)
        # glLoadIdentity()

        drawFullCube()
        #drawVertices()
        #drawEdges()

        pygame.display.flip()
        pygame.time.wait(10)

        glFlush()

# test_main()
