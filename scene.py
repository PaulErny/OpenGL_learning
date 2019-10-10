import logging

from OpenGL.GL import *
from OpenGL.GLU import *
import glfw
import numpy

from shape import *
import obj
import custom_shaders

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

    shader_program = custom_shaders.load_shaders()

    cube = Shape([4, 3, 3], shader_program, obj.cube_vertex_array, obj.cube_color_array)
    cube.init()

    triangle = Shape([4, 3, 3], shader_program, obj.triangle_vertices, obj.triangle_color)
    triangle.init()

    while not glfw.window_should_close(window) and glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS:
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        cube.draw()
        triangle.draw()

        glfw.swap_buffers(window)

    glfw.terminate()


main()
