import numpy
from OpenGL.GL import *
from OpenGL.GLU import *
import glm
import sys
import custom_shaders
from matrices import Matrices
from obj_parser import ObjParser


class Shape(Matrices):
    def __init__(self, cam_pos, shader_program, file_path=None, vertex_array=None, color_array=None):
        Matrices.__init__(self, cam_pos, shader_program)
        self.shader_program = shader_program
        self.color_buffer = None
        self.vbo = None
        self.normals_buffer = None

        if file_path is not None:
            self.obj = ObjParser()
            self.obj.get_shape(file_path)
            self.vertex_array = self.obj.out_vertices
            self.vertex_normals = self.obj.out_normals
        else:
            self.vertex_array = vertex_array
            self.vertex_normals = None
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
        if self.vertex_normals is not None:
            self.normals_buffer = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, self.normals_buffer)
            glBufferData(GL_ARRAY_BUFFER, sys.getsizeof(self.vertex_normals), self.vertex_normals, GL_STATIC_DRAW)

    def draw(self):
        glUseProgram(self.shader_program)
        glUniformMatrix4fv(self.matrixID, 1, GL_FALSE, glm.value_ptr(self.mvp_matrix))

        # normal buffer
        if self.vertex_normals is not None:
            glEnableVertexAttribArray(2)
            glBindBuffer(GL_ARRAY_BUFFER, self.normals_buffer)
            glVertexAttribPointer(2,
                                  3,
                                  GL_FLOAT,
                                  GL_FALSE,
                                  0,
                                  None)
        # color buffer
        if self.color_array is not None:
            glEnableVertexAttribArray(1)
            glBindBuffer(GL_ARRAY_BUFFER, self.color_buffer)
            glVertexAttribPointer(1,  # attribute. No particular reason for 1, but must match the layout in the shader.
                                  3,
                                  GL_FLOAT,
                                  GL_FALSE,
                                  0,
                                  None)
        # vertex buffer
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
        # normal end
        if self.vertex_normals is not None:
            glDisableVertexAttribArray(2)
