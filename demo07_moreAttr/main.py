#!/bin/python3

from pygame.locals import DOUBLEBUF
from pygame.locals import OPENGL
import OpenGL.GL as gl
import OpenGL.GLU as glu
import ctypes
import pygame

vertex_shader1 = """
#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;

out vec3 ourColor;

void main() {
    gl_Position = vec4(aPos, 1.0);
    ourColor = aColor;
}
"""

fragment_shader1 = """
#version 330 core
out vec4 FragColor;

in vec3 ourColor;

void main() {
    FragColor = vec4(ourColor, 1.0);
}
"""


def compileShader(shaderType, source):
    shader = gl.glCreateShader(shaderType)
    gl.glShaderSource(shader, source)
    gl.glCompileShader(shader)

    if not gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS):
        raise RuntimeError(gl.glGetShaderInfoLog(shader))

    return shader


def createShaderProgram(vertexSource, fragmentSource):
    vertexShader = compileShader(gl.GL_VERTEX_SHADER, vertexSource)
    fragmentShader = compileShader(gl.GL_FRAGMENT_SHADER, fragmentSource)

    shaderProgram = gl.glCreateProgram()
    gl.glAttachShader(shaderProgram, vertexShader)
    gl.glAttachShader(shaderProgram, fragmentShader)
    gl.glLinkProgram(shaderProgram)

    if not gl.glGetProgramiv(shaderProgram, gl.GL_LINK_STATUS):
        raise RuntimeError(gl.glGetProgramInfoLog(shaderProgram))

    gl.glDeleteShader(vertexShader)
    gl.glDeleteShader(fragmentShader)

    return shaderProgram


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glu.gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    gl.glTranslatef(0.0, 0.0, -5)

    VBO = gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VBO)

    data = [
        # 位置              # 颜色
        0.5, -0.5, 0.0,  1.0, 0.0, 0.0,   # 右下
        -0.5, -0.5, 0.0,  0.0, 1.0, 0.0,   # 左下
        0.0,  0.5, 0.0,  0.0, 0.0, 1.0    # 顶部
    ]
    gl.glBufferData(gl.GL_ARRAY_BUFFER,
                    ctypes.sizeof(ctypes.c_float) * len(data),
                    (gl.GLfloat * len(data))(*data),
                    gl.GL_STATIC_DRAW)

    VAO = gl.glGenVertexArrays(1)
    gl.glBindVertexArray(VAO)

    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE,
                             6 * ctypes.sizeof(ctypes.c_float),
                             ctypes.c_void_p(0))
    gl.glEnableVertexAttribArray(0)

    gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE,
                             6 * ctypes.sizeof(ctypes.c_float),
                             ctypes.c_void_p(3 * ctypes.sizeof(ctypes.c_float)))
    gl.glEnableVertexAttribArray(1)

    gl.glBindVertexArray(0)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

    shaderProgram = createShaderProgram(vertex_shader1, fragment_shader1)

    while True:
        processInput()

        gl.glClearColor(0.2, 0.3, 0.3, 1.0)
        gl.glClear(int(gl.GL_COLOR_BUFFER_BIT) | int(gl.GL_DEPTH_BUFFER_BIT))

        gl.glUseProgram(shaderProgram)

        gl.glBindVertexArray(VAO)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)
        gl.glBindVertexArray(0)

        pygame.display.flip()
        pygame.time.wait(30)


def processInput():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # exit windown
            pygame.quit()
            quit()


if __name__ == "__main__":
    main()
