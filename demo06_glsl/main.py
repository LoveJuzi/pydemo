#!/usr/bin/python3

from pygame.locals import DOUBLEBUF
from pygame.locals import OPENGL
import OpenGL.GL as gl
import OpenGL.GLU as glu
import ctypes
import math
import pygame

vertex_shader1 = """
#version 330 core
layout (location = 0) in vec3 aPos;
void main() {
    gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);
}
"""

fragment_shader1 = """
#version 330 core
out vec4 FragColor;

uniform vec4 ourColor;

void main() {
    FragColor = ourColor;
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

    data = [-0.5, -0.5, 0.0, 0.5, -0.5, 0.0, 0.0, 0.5, 0.0]
    gl.glBufferData(gl.GL_ARRAY_BUFFER,
                    ctypes.sizeof(ctypes.c_float) * len(data),
                    (gl.GLfloat * len(data))(*data),
                    gl.GL_STATIC_DRAW)

    VAO = gl.glGenVertexArrays(1)
    gl.glBindVertexArray(VAO)

    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE,
                             3 * ctypes.sizeof(ctypes.c_float),
                             ctypes.c_void_p(0))
    gl.glEnableVertexAttribArray(0)

    gl.glBindVertexArray(0)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

    shaderProgram = createShaderProgram(vertex_shader1, fragment_shader1)

    while True:
        processInput()

        gl.glClearColor(0.2, 0.3, 0.3, 1.0)
        gl.glClear(int(gl.GL_COLOR_BUFFER_BIT) | int(gl.GL_DEPTH_BUFFER_BIT))

        gl.glUseProgram(shaderProgram)

        timeValue = pygame.time.get_ticks()
        greenValue = math.sin(timeValue) / 2.0 + 0.5;

        vertexColorLocation = gl.glGetUniformLocation(shaderProgram, "ourColor")
        gl.glUniform4f(vertexColorLocation, 0.0, greenValue, 0.0, 1.0);

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
