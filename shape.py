import pygame
import numpy
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import glm
import sys
import custom_shaders


class Shape:
    def __init__(self, vertex_array, color_array):
        self.shader_program = None
        self.matrixID = None
        self.mvp_matrix = None
        self.color_buffer = None
        self.vbo = None
        self.vertex_array = vertex_array
        self.color_array = color_array

    def init(self):
        # Vertex buffer obj creation for the cube
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, sys.getsizeof(self.vertex_array), self.vertex_array, GL_STATIC_DRAW)

        # using custom shader to draw the vbo
        self.shader_program = custom_shaders.load_shaders()
        glUseProgram(self.shader_program)

        # Vertex buffer obj creation for cube's color
        self.color_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.color_buffer)
        glBufferData(GL_ARRAY_BUFFER, sys.getsizeof(self.color_array), self.color_array, GL_STATIC_DRAW)

        # creation of MVP matrix
        projection = glm.perspective(glm.radians(80.0), 4 / 3, 0.1, 100)
        # camera matrix
        view = glm.lookAt(glm.vec3(4, 3, 3), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
        # model matrix
        model = glm.mat4(1.0)
        self.mvp_matrix = projection * view * model
        # Giving the MVP matrix to GLSL
        self.matrixID = glGetUniformLocation(self.shader_program, "MVP")
        glUniformMatrix4fv(self.matrixID, 1, GL_FALSE, glm.value_ptr(self.mvp_matrix))

    def draw(self):
        glUseProgram(self.shader_program)
        glUniformMatrix4fv(self.matrixID, 1, GL_FALSE, glm.value_ptr(self.mvp_matrix))

        # color
        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.color_buffer)
        glVertexAttribPointer(1,  # attribute. No particular reason for 1, but must match the layout in the shader.
                              3,
                              GL_FLOAT,
                              GL_FALSE,
                              0,
                              None)
        # draw cube
        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
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
