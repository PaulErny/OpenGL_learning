import numpy
from OpenGL.GL import *
import glm


class Matrices:
    def __init__(self, cam_pos, shader_porgram):
        self.cam_pos = cam_pos
        self.shader_program = shader_porgram
        self.mvp_matrix = None
        self.matrixID = None

    def create_mvp(self):
        projection = glm.perspective(glm.radians(80.0), 4 / 3, 0.1, 100)
        # camera matrix
        view = glm.lookAt(glm.vec3(self.cam_pos[0], self.cam_pos[1], self.cam_pos[2]), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
        # model matrix
        model = glm.mat4(1.0)
        self.mvp_matrix = projection * view * model
        self.matrixID = glGetUniformLocation(self.shader_program, "MVP")
        glUniformMatrix4fv(self.matrixID, 1, GL_FALSE, glm.value_ptr(self.mvp_matrix))

    def rotate(self):
        pass

    def translate(self):
        pass

    def scale(self):
        pass
