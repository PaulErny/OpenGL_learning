import numpy
from OpenGL.GL import *
import glfw
import glm


class Matrices:
    def __init__(self, cam_pos, shader_porgram):
        self.cam_pos = cam_pos
        self.shader_program = shader_porgram
        self.mvp_matrix = None
        self.matrixID = None

    def compute_mvp(self, position=[4, 3, 3], direction=[0, 0, 0], up=[0, 1, 0]):
        projection = glm.perspective(glm.radians(80.0), 4 / 3, 0.1, 100)
        # camera matrix
        view = glm.lookAt(glm.vec3(position[0], position[1], position[2]),
                          glm.vec3(direction[0], direction[1], direction[2]),
                          glm.vec3(up[0], up[1], up[2]))
        # model matrix
        model = glm.mat4(1.0)
        self.mvp_matrix = projection * view * model
        self.matrixID = glGetUniformLocation(self.shader_program, "MVP")
        glUniformMatrix4fv(self.matrixID, 1, GL_FALSE, glm.value_ptr(self.mvp_matrix))
        self.matrixID = glGetUniformLocation(self.shader_program, "M")
        glUniformMatrix4fv(self.matrixID, 1, GL_FALSE, glm.value_ptr(model))
        self.matrixID = glGetUniformLocation(self.shader_program, "V")
        glUniformMatrix4fv(self.matrixID, 1, GL_FALSE, glm.value_ptr(view))

    def rotate(self):
        pass

    def translate(self):
        pass

    def scale(self):
        pass
