#!/bin/python3

import pygame
from pygame.locals import DOUBLEBUF
from pygame.locals import OPENGL
import OpenGL.GL as gl
import OpenGL.GLU as glu
# from pygame.locals import *
# from OpenGL.GL import *
# from OpenGL.GLU import *

vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

edges = (
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7)
)

# 两个简单的顶点着色器
vertex_shader1 = """
#version 330 core
layout (location = 0) in vec3 aPos;
void main() {
    gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);
}
"""

vertex_shader2 = """
#version 330 core
layout (location = 0) in vec3 aPos;
void main() {
    gl_Position = vec4(aPos.x * 1.5, aPos.y * 1.5, aPos.z * 1.5, 1.0);
}
"""

# 两个简单的片段着色器
fragment_shader1 = """
#version 330 core
out vec4 FragColor;
void main() {
    FragColor = vec4(1.0, 0.5, 0.2, 1.0);
}
"""

fragment_shader2 = """
#version 330 core
out vec4 FragColor;
void main() {
    FragColor = vec4(0.2, 0.5, 1.0, 1.0);
}
"""


def compile_shader(shader_type, source):
    shader = gl.glCreateShader(shader_type)
    gl.glShaderSource(shader, source)
    gl.glCompileShader(shader)
    if not gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS):
        raise RuntimeError(gl.glGetShaderInfoLog(shader))
    return shader


def create_shader_program(vertex_source, fragment_source):
    vertex_shader = compile_shader(gl.GL_VERTEX_SHADER, vertex_source)
    fragment_shader = compile_shader(gl.GL_FRAGMENT_SHADER, fragment_source)

    shader_program = gl.glCreateProgram()
    gl.glAttachShader(shader_program, vertex_shader)
    gl.glAttachShader(shader_program, fragment_shader)
    gl.glLinkProgram(shader_program)

    if not gl.glGetProgramiv(shader_program, gl.GL_LINK_STATUS):
        raise RuntimeError(gl.glGetProgramInfoLog(shader_program))

    gl.glDeleteShader(vertex_shader)
    gl.glDeleteShader(fragment_shader)

    return shader_program


def draw_cube():
    gl.glBegin(gl.GL_LINES)
    for edge in edges:
        for vertex in edge:
            gl.glVertex3fv(vertices[vertex])
    gl.glEnd()

# def draw_cube(shader_program):
#    gl.glBegin(gl.GL_LINES)
#    for edge in edges:
#        for vertex in edge:
#            gl.glVertex3fv(vertices[vertex])
#    gl.glEnd()


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glu.gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    gl.glTranslatef(0.0, 0.0, -5)

    shader_program1 = create_shader_program(vertex_shader1, fragment_shader1)
    shader_program2 = create_shader_program(vertex_shader2, fragment_shader2)

    current_shader_program = shader_program1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # 切换着色器程序
                    current_shader_program = shader_program2 if current_shader_program == shader_program1 else shader_program1

        gl.glRotatef(1, 3, 1, 1)
        gl.glClear(int(gl.GL_COLOR_BUFFER_BIT) | int(gl.GL_DEPTH_BUFFER_BIT))
        gl.glUseProgram(current_shader_program)
        # draw_cube(current_shader_program)
        draw_cube()
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    main()
