import numpy
from OpenGL.GL import *
from OpenGL.GLU import *
import glm
import sys
import custom_shaders
from matrices import Matrices


class Shape(Matrices):
    def __init__(self, cam_pos, shader_program, vertex_array, color_array=None):
        Matrices.__init__(self, cam_pos, shader_program)
        self.shader_program = shader_program
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
        glUseProgram(self.shader_program)

        # Vertex buffer obj creation for cube's color
        if self.color_array is not None:
            self.color_buffer = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, self.color_buffer)
            glBufferData(GL_ARRAY_BUFFER, sys.getsizeof(self.color_array), self.color_array, GL_STATIC_DRAW)

        # creation of MVP matrix
        self.create_mvp()

    def draw(self):
        glUseProgram(self.shader_program)
        glUniformMatrix4fv(self.matrixID, 1, GL_FALSE, glm.value_ptr(self.mvp_matrix))

        # color
        if self.color_array is not None:
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

        glDrawArrays(GL_TRIANGLES, 0, len(self.vertex_array))
        glDisableVertexAttribArray(0)
        # color end
        if self.color_array is not None:
            glDisableVertexAttribArray(1)
