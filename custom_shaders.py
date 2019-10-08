from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GL.shaders import *
import numpy, math

def load_shaders():
    vertex_shader_id = glCreateShader(GL_VERTEX_SHADER)
    fragment_shader_id = glCreateShader(GL_FRAGMENT_SHADER)

    vertexShaderCode = """
            #version 330 core

            layout(location = 0) in vec3 vertexPosition_modelspace;
            
            void main() {
              gl_Position.xyz = vertexPosition_modelspace;
              gl_Position.w = 1.0;
            }
        """

    # fragment shader program
    fragmentShaderCode = """
            #version 330 core
            out vec3 color;
            void main(){
              color = vec3(1,0,0);
            }
        """

    vs = compileShader(vertexShaderCode, GL_VERTEX_SHADER)
    fs = compileShader(fragmentShaderCode, GL_FRAGMENT_SHADER)
    program = compileProgram(vs, fs)
    return program
