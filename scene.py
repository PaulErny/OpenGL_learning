import glfw
import logging
import sys
import numpy
import cube
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
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(80, 800 / 600, 0.1, 500)  # fov
    glEnable(GL_DEPTH_TEST)  # explicit

    # Vertex array obj creation
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vertex_array = numpy.array([[-1.0, -1.0, 0.0], [1.0, -1.0, 0.0], [0.0,  1.0, 0.0]], dtype='f')

    # Vertex buffer obj creation
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, sys.getsizeof(vertex_array), vertex_array, GL_STATIC_DRAW)

    # using custom shader to draw the vbo
    shader_program = custom_shaders.load_shaders()
    glUseProgram(shader_program)

    # creation of MVP matrix
    projection = glm.perspective(glm.radians(80.0), 4/3, 0.1, 100)
    # camera matrix
    view = glm.lookAt(glm.vec3(4, 3, 3), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
    # model matrix
    model = glm.mat4(1.0)
    mvp_matrix = projection * view * model
    # Giving the MVP matrix to GLSL
    matrixID = glGetUniformLocation(shader_program, "MVP")
    glUniformMatrix4fv(matrixID, 1, GL_FALSE, glm.value_ptr(mvp_matrix))

    while not glfw.window_should_close(window) and glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS:
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(shader_program)
        glUniformMatrix4fv(matrixID, 1, GL_FALSE, glm.value_ptr(mvp_matrix))

        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glDisableVertexAttribArray(0)

        glfw.swap_buffers(window)

    glfw.terminate()


main()
