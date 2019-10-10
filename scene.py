import glfw
import logging
import numpy
import shape
#from cube import *
from ctypes import *
import time
from FreeCam import FreeCam
import custom_shaders
from OpenGL.GL import *
from OpenGL.GLU import *
import glm

# visit https://rdmilligan.wordpress.com/2016/08/27/opengl-shaders-using-python/ for python OpenGL shader example

def main():
    # glfw init
    if not glfw.init():
        logging.error("glfw init failed")
        exit(0)

    glfw.window_hint(glfw.SAMPLES, 4)
    glfw.window_hint(glfw.DOUBLEBUFFER, GL_TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_ANY_PROFILE)

    window = glfw.create_window(1024, 768, "3D", None, None)
    if not window:
        logging.error("Couldn't create window")
        glfw.terminate()
        exit(0)
    glfw.make_context_current(window)
    glfw.set_input_mode(window, glfw.STICKY_KEYS, GL_TRUE)

    # OpenGL init
    glEnable(GL_DEPTH_TEST)  # explicit
    glDepthFunc(GL_LESS)

    # Vertex array obj creation
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    shape.init_colored_cube()

    while not glfw.window_should_close(window) and glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS:
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        shape.draw()

        glfw.swap_buffers(window)

    glfw.terminate()


main()
