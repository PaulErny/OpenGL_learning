from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GL.shaders import *
import numpy, math

def load_shaders():
    vertex_shader_id = glCreateShader(GL_VERTEX_SHADER)
    fragment_shader_id = glCreateShader(GL_FRAGMENT_SHADER)

    vertexShaderCode = """
            #version 330 core

            // Notice that the "0" here equals the "0" in glVertexAttribPointer
            layout(location = 0) in vec3 vertexPosition_modelspace;
            // Notice that the "1" here equals the "1" in glVertexAttribPointer
            layout(location = 1) in vec3 vertexColor;
            
            out vec3 fragmentColor;
            uniform mat4 MVP;
            
            void main() {
              gl_Position =  MVP * vec4(vertexPosition_modelspace,1);
              
              // The color of each vertex will be interpolated
              // to produce the color of each fragment
              fragmentColor = vertexColor;
            }
        """

    # fragment shader program
    fragmentShaderCode = """
            #version 330 core
            
            // Interpolated values from the vertex shaders
            in vec3 fragmentColor;
            out vec3 color;
            
            void main(){
              // Output color = color specified in the vertex shader,
              // interpolated between all 3 surrounding vertices
              color = fragmentColor;
            }
        """

    vs = compileShader(vertexShaderCode, GL_VERTEX_SHADER)
    fs = compileShader(fragmentShaderCode, GL_FRAGMENT_SHADER)
    program = compileProgram(vs, fs)
    return program
