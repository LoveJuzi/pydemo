#!/usr/bin/python3

import numpy as np
from pygame.locals import DOUBLEBUF
from pygame.locals import OPENGL
from res import resourceFile
from shader import Shader
import OpenGL.GL as gl
import OpenGL.GLU as glu
import ctypes
import pygame
from PIL import Image


def load_texture():
    tid = gl.glGenTextures(1)

    gl.glBindTexture(gl.GL_TEXTURE_2D, tid)

    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
    gl.glTexParameteri(
        gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
    gl.glTexParameteri(
        gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)

    img = Image.open(resourceFile("container.jpg"))
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, img.width,
                    img.height, 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, img.tobytes())
    gl.glGenerateMipmap(gl.GL_TEXTURE_2D)
    return tid


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glu.gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    gl.glTranslatef(0.0, 0.0, -5)

    # data = np.array([
    #    # 位置              # 颜色
    #    0.5, -0.5, 0.0,  1.0, 0.0, 0.0,   # 右下
    #    -0.5, -0.5, 0.0,  0.0, 1.0, 0.0,   # 左下
    #    0.0,  0.5, 0.0,  0.0, 0.0, 1.0    # 顶部
    # ], dtype=np.float32)

    data = np.array([
        #     ---- 位置 ----       ---- 颜色 ----     - 纹理坐标 -
        0.5,  0.5, 0.0,   1.0, 0.0, 0.0,   1.0, 1.0,   # 右上
        0.5, -0.5, 0.0,   0.0, 1.0, 0.0,   1.0, 0.0,   # 右下
        -0.5,  0.5, 0.0,   1.0, 1.0, 0.0,   0.0, 1.0,    # 左上

        0.5, -0.5, 0.0,   0.0, 1.0, 0.0,   1.0, 0.0,   # 右下
        -0.5, -0.5, 0.0,   0.0, 0.0, 1.0,   0.0, 0.0,   # 左下
        -0.5,  0.5, 0.0,   1.0, 1.0, 0.0,   0.0, 1.0,    # 左上
    ], dtype=np.float32)

    # data = [
    #    #     ---- 位置 ----       ---- 颜色 ----     - 纹理坐标 -
    #    0.5,  0.5, 0.0,   1.0, 0.0, 0.0,   1.0, 1.0,   # 右上
    #    0.5, -0.5, 0.0,   0.0, 1.0, 0.0,   1.0, 0.0,   # 右下
    #    -0.5, -0.5, 0.0,   0.0, 0.0, 1.0,   0.0, 0.0,   # 左下
    #    -0.5,  0.5, 0.0,   1.0, 1.0, 0.0,   0.0, 1.0,    # 左上

    # ]

    # indices = np.array([
    #    # 0, 1, 2,  # 第一个三角形
    #    # 1, 2, 3  # 第二个三角形
    # ], dtype=np.uint32)

    VAO = gl.glGenVertexArrays(1)
    gl.glBindVertexArray(VAO)

    VBO = gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VBO)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, data.nbytes, data, gl.GL_STATIC_DRAW)

    # EBO = gl.glGenBuffers(1)
    # gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, EBO)
    # gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER,
    #                indices.nbytes, indices, gl.GL_STATIC_DRAW)

    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE,
                             8 * ctypes.sizeof(ctypes.c_float),
                             ctypes.c_void_p(0))
    gl.glEnableVertexAttribArray(0)

    gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE,
                             8 * ctypes.sizeof(ctypes.c_float),
                             ctypes.c_void_p(3 * ctypes.sizeof(ctypes.c_float)))
    gl.glEnableVertexAttribArray(1)

    gl.glVertexAttribPointer(2, 2, gl.GL_FLOAT, gl.GL_FALSE,
                             8 * ctypes.sizeof(ctypes.c_float),
                             ctypes.c_void_p(6 * ctypes.sizeof(ctypes.c_float)))
    gl.glEnableVertexAttribArray(2)

    gl.glBindVertexArray(0)
    # gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, 0)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

    shader = Shader().init(resourceFile("shader10.vs"), resourceFile("shader10.fs"))

    texture = load_texture()

    while processInput():

        gl.glClearColor(0.2, 0.3, 0.3, 1.0)
        gl.glClear(int(gl.GL_COLOR_BUFFER_BIT) | int(gl.GL_DEPTH_BUFFER_BIT))

        shader.use()

        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
        gl.glBindVertexArray(VAO)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 6)
        # gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, EBO);
        # gl.glDrawElements(gl.GL_TRIANGLES, 3, gl.GL_UNSIGNED_INT, 0)
        # gl.glDrawElements(gl.GL_TRIANGLES, 3, gl.GL_UNSIGNED_INT, 0)
        gl.glBindVertexArray(0)

        pygame.display.flip()
        pygame.time.wait(30)

    # gl.glDeleteBuffers(1, VBO)
    # gl.glDeleteVertexArrays(1, VAO)

    pygame.quit()


def processInput():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

    return True


if __name__ == "__main__":
    main()
