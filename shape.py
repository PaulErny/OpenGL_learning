import pygame
import numpy
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import glm
import sys
import custom_shaders


shader_program = None
matrixID = None
mvp_matrix = None
color_buffer = None
vbo = None


def init_colored_cube():
    global shader_program
    global matrixID
    global mvp_matrix
    global color_buffer
    global vbo

    vertex_array = numpy.array([[-1.0, -1.0, -1.0],  # triangle 1 : begin
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

    # Vertex buffer obj creation for the cube
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, sys.getsizeof(vertex_array), vertex_array, GL_STATIC_DRAW)

    # using custom shader to draw the vbo
    shader_program = custom_shaders.load_shaders()
    glUseProgram(shader_program)

    color_array = numpy.array([[0.583, 0.771, 0.014],
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

    # Vertex buffer obj creation for cube's color
    color_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, color_buffer)
    glBufferData(GL_ARRAY_BUFFER, sys.getsizeof(color_array), color_array, GL_STATIC_DRAW)

    # creation of MVP matrix
    projection = glm.perspective(glm.radians(80.0), 4 / 3, 0.1, 100)
    # camera matrix
    view = glm.lookAt(glm.vec3(4, 3, 3), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
    # model matrix
    model = glm.mat4(1.0)
    mvp_matrix = projection * view * model
    # Giving the MVP matrix to GLSL
    matrixID = glGetUniformLocation(shader_program, "MVP")
    glUniformMatrix4fv(matrixID, 1, GL_FALSE, glm.value_ptr(mvp_matrix))


def draw():
    global shader_program
    global matrixID
    global mvp_matrix
    global color_buffer
    global vbo

    glUseProgram(shader_program)
    glUniformMatrix4fv(matrixID, 1, GL_FALSE, glm.value_ptr(mvp_matrix))

    # color
    glEnableVertexAttribArray(1)
    glBindBuffer(GL_ARRAY_BUFFER, color_buffer)
    glVertexAttribPointer(1,  # attribute. No particular reason for 1, but must match the layout in the shader.
                          3,
                          GL_FLOAT,
                          GL_FALSE,
                          0,
                          None)
    # draw cube
    glEnableVertexAttribArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glVertexAttribPointer(0,  # attribute. No particular reason for 0, but must match the layout in the shader.
                          3,
                          GL_FLOAT,
                          GL_FALSE,
                          0,
                          None)
    glDrawArrays(GL_TRIANGLES, 0, 12 * 3)
    glDisableVertexAttribArray(0)
    # color end
    glDisableVertexAttribArray(1)
