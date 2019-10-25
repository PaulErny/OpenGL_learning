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
            layout(location = 2) in vec3 vertexNormal_modelspace;
            
            out vec3 fragmentColor;
            out vec3 LightDirection_cameraspace;
            out vec3 Normal_cameraspace;
            out float distance;
            uniform mat4 MVP;
            uniform mat4 M;
            uniform mat4 V;
            
            void main() {
              gl_Position =  MVP * vec4(vertexPosition_modelspace,1);
              
              vec3 LightPosition_worldspace = vec3(1, 7, 1);
              distance = sqrt(pow(LightPosition_worldspace.x - vertexPosition_modelspace.x, 2) + 
                              pow(LightPosition_worldspace.y - vertexPosition_modelspace.y, 2) + 
                              pow(LightPosition_worldspace.z - vertexPosition_modelspace.z, 2));
              // Position of the vertex, in worldspace : M * position
              vec3 Position_worldspace = (M * vec4(vertexPosition_modelspace,1)).xyz;
              
              // Vector that goes from the vertex to the camera, in camera space.
              // In camera space, the camera is at the origin (0,0,0).
              vec3 vertexPosition_cameraspace = ( V * M * vec4(vertexPosition_modelspace,1)).xyz;
              vec3 EyeDirection_cameraspace = vec3(0,0,0) - vertexPosition_cameraspace;
              
              // Vector that goes from the vertex to the light, in camera space. M is ommited because it's identity.
              vec3 LightPosition_cameraspace = ( V * vec4(LightPosition_worldspace,1)).xyz;
              LightDirection_cameraspace = LightPosition_cameraspace + EyeDirection_cameraspace;
              
              // Normal of the the vertex, in camera space
              Normal_cameraspace = ( V * M * vec4(vertexNormal_modelspace,0)).xyz; // Only correct if ModelMatrix does not scale the model ! Use its inverse transpose if not.
              
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
            in vec3 LightDirection_cameraspace;
            in vec3 Normal_cameraspace;
            in float distance;
            out vec3 color;
            
            void main(){
              int lightPower = 60;
              // Normal of the computed fragment, in camera space
              vec3 n = normalize( Normal_cameraspace );
              // Direction of the light (from the fragment to the light)
              vec3 l = normalize( LightDirection_cameraspace );
              vec3 lightColor = vec3(1, 1, 1);
              vec3 MaterialAmbientColor = vec3(0.1,0.1,0.1) * fragmentColor;
              float cosTheta = clamp( dot(n, l), 0, 1);
              
              // Output color = color specified in the vertex shader,
              // interpolated between all 3 surrounding vertices
              color = MaterialAmbientColor + fragmentColor * lightColor * lightPower * cosTheta / (distance * distance);  //cosTheta should be devided by distance * distance
            }
        """

    vs = compileShader(vertexShaderCode, GL_VERTEX_SHADER)
    fs = compileShader(fragmentShaderCode, GL_FRAGMENT_SHADER)
    program = compileProgram(vs, fs)
    return program
