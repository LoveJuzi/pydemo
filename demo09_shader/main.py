#!/bin/python3

from pygame.locals import DOUBLEBUF
from pygame.locals import OPENGL
from res import resourceFile
from shader import Shader
import OpenGL.GL as gl
import OpenGL.GLU as glu
import ctypes
import pygame


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

    shader = Shader().init(resourceFile("shader.vs"), resourceFile("shader.fs"))

    while True:
        processInput()

        gl.glClearColor(0.2, 0.3, 0.3, 1.0)
        gl.glClear(int(gl.GL_COLOR_BUFFER_BIT) | int(gl.GL_DEPTH_BUFFER_BIT))

        shader.use()

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
