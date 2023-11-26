#!/bin/python3

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

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
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        raise RuntimeError(glGetShaderInfoLog(shader))
    return shader

def create_shader_program(vertex_source, fragment_source):
    vertex_shader = compile_shader(GL_VERTEX_SHADER, vertex_source)
    fragment_shader = compile_shader(GL_FRAGMENT_SHADER, fragment_source)

    shader_program = glCreateProgram()
    glAttachShader(shader_program, vertex_shader)
    glAttachShader(shader_program, fragment_shader)
    glLinkProgram(shader_program)

    if not glGetProgramiv(shader_program, GL_LINK_STATUS):
        raise RuntimeError(glGetProgramInfoLog(shader_program))

    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    return shader_program

def draw_cube(shader_program):
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

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

        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(current_shader_program)
        draw_cube(current_shader_program)
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()

