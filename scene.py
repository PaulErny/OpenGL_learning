import glfw
import logging
import numpy
from shape import *
from ctypes import *
import time
from FreeCam import FreeCam
import custom_shaders
from OpenGL.GL import *
from OpenGL.GLU import *
import glm

# visit https://rdmilligan.wordpress.com/2016/08/27/opengl-shaders-using-python/ for python OpenGL shader example

triangle_vertices = numpy.array([[2.0, 0.0, -1.0],
                                 [0.0, 0.0, -1.0],
                                 [0.0,  2.0, -1.0]],
                                dtype='f')

triangle_color = numpy.array([[1.0, 0.0, 0.0],
                              [1.0, 0.0, 0.0],
                              [1.0,  0.0, 0.0]],
                             dtype='f')

cube_vertex_array = numpy.array([[-1.0, -1.0, -1.0],  # triangle 1 : begin
                                 [-1.0, -1.0, 1.0],
                                 [-1.0, 1.0, 1.0],  # triangle 1 : end
                                 [1.0, 1.0, -1.0],  # triangle 2 : begin
                                 [-1.0, -1.0, -1.0],
                                 [-1.0, 1.0, -1.0],  # triangle 2 : end
                                 [1.0, -1.0, 1.0],
                                 [-1.0, -1.0, -1.0],
                                 [1.0, -1.0, -1.0],
                                 [1.0, 1.0, -1.0],
                                 [1.0, -1.0, -1.0],
                                 [-1.0, -1.0, -1.0],
                                 [-1.0, -1.0, -1.0],
                                 [-1.0, 1.0, 1.0],
                                 [-1.0, 1.0, -1.0],
                                 [1.0, -1.0, 1.0],
                                 [-1.0, -1.0, 1.0],
                                 [-1.0, -1.0, -1.0],
                                 [-1.0, 1.0, 1.0],
                                 [-1.0, -1.0, 1.0],
                                 [1.0, -1.0, 1.0],
                                 [1.0, 1.0, 1.0],
                                 [1.0, -1.0, -1.0],
                                 [1.0, 1.0, -1.0],
                                 [1.0, -1.0, -1.0],
                                 [1.0, 1.0, 1.0],
                                 [1.0, -1.0, 1.0],
                                 [1.0, 1.0, 1.0],
                                 [1.0, 1.0, -1.0],
                                 [-1.0, 1.0, -1.0],
                                 [1.0, 1.0, 1.0],
                                 [-1.0, 1.0, -1.0],
                                 [-1.0, 1.0, 1.0],
                                 [1.0, 1.0, 1.0],
                                 [-1.0, 1.0, 1.0],
                                 [1.0, -1.0, 1.0]],
                                dtype='f')

cube_color_array = numpy.array([[0.583, 0.771, 0.014],
                                [0.609, 0.115, 0.436],
                                [0.327, 0.483, 0.844],
                                [0.822, 0.569, 0.201],
                                [0.435, 0.602, 0.223],
                                [0.310, 0.747, 0.185],
                                [0.597, 0.770, 0.761],
                                [0.559, 0.436, 0.730],
                                [0.359, 0.583, 0.152],
                                [0.483, 0.596, 0.789],
                                [0.559, 0.861, 0.639],
                                [0.195, 0.548, 0.859],
                                [0.014, 0.184, 0.576],
                                [0.771, 0.328, 0.970],
                                [0.406, 0.615, 0.116],
                                [0.676, 0.977, 0.133],
                                [0.971, 0.572, 0.833],
                                [0.140, 0.616, 0.489],
                                [0.997, 0.513, 0.064],
                                [0.945, 0.719, 0.592],
                                [0.543, 0.021, 0.978],
                                [0.279, 0.317, 0.505],
                                [0.167, 0.620, 0.077],
                                [0.347, 0.857, 0.137],
                                [0.055, 0.953, 0.042],
                                [0.714, 0.505, 0.345],
                                [0.783, 0.290, 0.734],
                                [0.722, 0.645, 0.174],
                                [0.302, 0.455, 0.848],
                                [0.225, 0.587, 0.040],
                                [0.517, 0.713, 0.338],
                                [0.053, 0.959, 0.120],
                                [0.393, 0.621, 0.362],
                                [0.673, 0.211, 0.457],
                                [0.820, 0.883, 0.371],
                                [0.982, 0.099, 0.879]],
                               dtype='f')


def main():
    global vertex_array
    global color_array
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

    cube = Shape(cube_vertex_array, cube_color_array)
    cube.init()

    triangle = Shape(triangle_vertices, triangle_color)
    triangle.init()

    while not glfw.window_should_close(window) and glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS:
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        cube.draw()
        triangle.draw()

        glfw.swap_buffers(window)

    glfw.terminate()


main()
