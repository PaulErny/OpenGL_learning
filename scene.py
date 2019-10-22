import logging
import math

from OpenGL.GL import *
from OpenGL.GLU import *
import glfw
import glm
import numpy

from shape import *
import obj
import custom_shaders
from matrices import Matrices
from check_opti import CheckOpti

# visit https://rdmilligan.wordpress.com/2016/08/27/opengl-shaders-using-python/ for python OpenGL shader example

position = glm.vec3(0, 0, 5)
horizontal_angle = 3.14
vertical_angle = 0.0


def compute_matrices_from_inputs(window, elapsed):
    global position
    global horizontal_angle
    global vertical_angle
    speed = 10.0
    mouse_speed = 0.005

    mouse_pos = glfw.get_cursor_pos(window)
    glfw.set_cursor_pos(window, 1024 / 2, 768 / 2)
    horizontal_angle += mouse_speed * float(1024 / 2 - mouse_pos[0])
    vertical_angle += mouse_speed * float(768 / 2 - mouse_pos[1])

    direction = glm.vec3(math.cos(vertical_angle) * math.sin(horizontal_angle),
                         math.sin(vertical_angle),
                         math.cos(vertical_angle) * math.cos(horizontal_angle))

    right = glm.vec3(math.sin(horizontal_angle - 3.14 / 2.0),
                     0,
                     math.cos(horizontal_angle - 3.14 / 2.0))

    up = glm.cross(right, direction)

    if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
        position += direction * speed * elapsed
    if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
        position -= direction * speed * elapsed
    if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
        position += right * speed * elapsed
    if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
        position -= right * speed * elapsed

    return [position, position + direction, up]

def main():
    opti = CheckOpti()
    opti.start()

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
    glEnable(GL_DEPTH_TEST)  # explicit
    glDepthFunc(GL_LESS)
    # enabling backface culling to draw only the triangles facing the camera
    glEnable(GL_CULL_FACE)  # if there are holes in models => invert normals / vertices in 3D modeler (blender, ...)

    # Vertex array obj creation
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    shader_program = custom_shaders.load_shaders()

    cube = Shape([4, 3, 3], shader_program, file_path="resources/cube.obj", color_array=obj.cube_color_array)
    cube.init()

    triangle = Shape([4, 3, 3], shader_program, vertex_array=obj.triangle_vertices, color_array=obj.triangle_color)
    triangle.init()

    start = glfw.get_time()
    glfw.set_cursor_pos(window, 1024 / 2, 768 / 2)

    while not glfw.window_should_close(window) and glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS:
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        matrices = compute_matrices_from_inputs(window, glfw.get_time() - start)
        cube.compute_mvp(matrices[0], matrices[1], matrices[2])
        triangle.compute_mvp(matrices[0], matrices[1], matrices[2])

        cube.draw()
        triangle.draw()

        glfw.swap_buffers(window)
        start = glfw.get_time()
        break  # rm after optimization checked

    glfw.terminate()
    opti.end()


if __name__ == '__main__':
    main()
