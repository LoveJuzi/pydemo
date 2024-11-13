#!/usr/bin/python3

from pygame.locals import DOUBLEBUF
from pygame.locals import OPENGL
from res import loadTexture
from res import resourceFile
from shader import Shader
import OpenGL.GL as gl
import ctypes
import glm
import numpy as np
import pygame


def buildTransform(screenWidth, screenHeight):
    model = glm.mat4()
    model = glm.rotate(model, glm.radians(-55), glm.vec3(1, 0, 0))

    view = glm.mat4()
    view = glm.translate(view, glm.vec3(0, 0, -3))

    projection = glm.mat4()
    projection = glm.perspective(glm.radians(
        45), screenWidth/screenHeight, 0.1, 100)

    return model, view, projection


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    data = np.array([
        #     ---- 位置 ----       ---- 颜色 ----     - 纹理坐标 -
        # 0.5,  0.5, 0.0,     1.0, 1.0,   # 右上
        # 0.5, -0.5, 0.0,     1.0, 0.0,   # 右下
        # -0.5,  0.5, 0.0,     0.0, 1.0,    # 左上

        # 0.5, -0.5, 0.0,    1.0, 0.0,   # 右下
        # -0.5, -0.5, 0.0,    0.0, 0.0,   # 左下
        # -0.5,  0.5, 0.0,    0.0, 1.0,    # 左上

        -0.5, -0.5, -0.5,  0.0, 0.0,
        0.5, -0.5, -0.5,  1.0, 0.0,
        0.5,  0.5, -0.5,  1.0, 1.0,
        0.5,  0.5, -0.5,  1.0, 1.0,
        -0.5,  0.5, -0.5,  0.0, 1.0,
        -0.5, -0.5, -0.5,  0.0, 0.0,

        -0.5, -0.5,  0.5,  0.0, 0.0,
        0.5, -0.5,  0.5,  1.0, 0.0,
        0.5,  0.5,  0.5,  1.0, 1.0,
        0.5,  0.5,  0.5,  1.0, 1.0,
        -0.5,  0.5,  0.5,  0.0, 1.0,
        -0.5, -0.5,  0.5,  0.0, 0.0,

        -0.5,  0.5,  0.5,  1.0, 0.0,
        -0.5,  0.5, -0.5,  1.0, 1.0,
        -0.5, -0.5, -0.5,  0.0, 1.0,
        -0.5, -0.5, -0.5,  0.0, 1.0,
        -0.5, -0.5,  0.5,  0.0, 0.0,
        -0.5,  0.5,  0.5,  1.0, 0.0,

        0.5,  0.5,  0.5,  1.0, 0.0,
        0.5,  0.5, -0.5,  1.0, 1.0,
        0.5, -0.5, -0.5,  0.0, 1.0,
        0.5, -0.5, -0.5,  0.0, 1.0,
        0.5, -0.5,  0.5,  0.0, 0.0,
        0.5,  0.5,  0.5,  1.0, 0.0,

        -0.5, -0.5, -0.5,  0.0, 1.0,
        0.5, -0.5, -0.5,  1.0, 1.0,
        0.5, -0.5,  0.5,  1.0, 0.0,
        0.5, -0.5,  0.5,  1.0, 0.0,
        -0.5, -0.5,  0.5,  0.0, 0.0,
        -0.5, -0.5, -0.5,  0.0, 1.0,

        -0.5,  0.5, -0.5,  0.0, 1.0,
        0.5,  0.5, -0.5,  1.0, 1.0,
        0.5,  0.5,  0.5,  1.0, 0.0,
        0.5,  0.5,  0.5,  1.0, 0.0,
        -0.5,  0.5,  0.5,  0.0, 0.0,
        -0.5,  0.5, -0.5,  0.0, 1.0
    ], dtype=np.float32)

    # data = np.array([
    #    #     ---- 位置 ----       ---- 颜色 ----     - 纹理坐标 -
    #    0.5,  0.5, 0.0,   1.0, 0.0, 0.0,   1.0, 1.0,   # 右上
    #    0.5, -0.5, 0.0,   0.0, 1.0, 0.0,   1.0, 0.0,   # 右下
    #    -0.5,  0.5, 0.0,   1.0, 1.0, 0.0,   0.0, 1.0,    # 左上

    #    0.5, -0.5, 0.0,   0.0, 1.0, 0.0,   1.0, 0.0,   # 右下
    #    -0.5, -0.5, 0.0,   0.0, 0.0, 1.0,   0.0, 0.0,   # 左下
    #    -0.5,  0.5, 0.0,   1.0, 1.0, 0.0,   0.0, 1.0,    # 左上
    # ], dtype=np.float32)

    VAO = gl.glGenVertexArrays(1)
    gl.glBindVertexArray(VAO)

    VBO = gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VBO)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, data.nbytes, data, gl.GL_STATIC_DRAW)

    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE,
                             5 * ctypes.sizeof(ctypes.c_float),
                             ctypes.c_void_p(0))
    gl.glEnableVertexAttribArray(0)

    # gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE,
    #                         8 * ctypes.sizeof(ctypes.c_float),
    #                         ctypes.c_void_p(3 * ctypes.sizeof(ctypes.c_float)))
    # gl.glEnableVertexAttribArray(1)

    gl.glVertexAttribPointer(1, 2, gl.GL_FLOAT, gl.GL_FALSE,
                             5 * ctypes.sizeof(ctypes.c_float),
                             ctypes.c_void_p(3 * ctypes.sizeof(ctypes.c_float)))
    gl.glEnableVertexAttribArray(1)

    gl.glBindVertexArray(0)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

    shader = Shader().init(resourceFile("shader14.vs"), resourceFile("shader14.fs"))

    texture1 = loadTexture(resourceFile("container.jpg"))
    texture2 = loadTexture(resourceFile("awesomeface.png"))

    shader.use()
    shader.setInt("texture1", 0)
    shader.setInt("texture2", 1)

    model, view, projection = buildTransform(*display)

    gl.glEnable(gl.GL_DEPTH_TEST)

    clock = pygame.time.Clock()

    while processInput():

        gl.glClearColor(0.2, 0.3, 0.3, 1.0)
        gl.glClear(int(gl.GL_COLOR_BUFFER_BIT) | int(gl.GL_DEPTH_BUFFER_BIT))

        model = glm.rotate(glm.mat4(),
                           pygame.time.get_ticks() / 1000 * glm.radians(50.0),
                           glm.vec3(0.5, 1.0, 0.0))

        shader.use()

        shader.setMat4("model", model)
        shader.setMat4("view", view)
        shader.setMat4("projection", projection)

        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, texture1)
        gl.glActiveTexture(gl.GL_TEXTURE1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, texture2)

        gl.glBindVertexArray(VAO)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, len(data))
        gl.glBindVertexArray(0)

        pygame.display.flip()
        # pygame.time.wait(30)
        clock.tick(60)

    gl.glDeleteVertexArrays(1, VAO)
    gl.glDeleteBuffers(1, VBO)
    gl.glDeleteTextures(1, texture1)
    gl.glDeleteTextures(1, texture2)

    pygame.quit()


def processInput():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

    return True


if __name__ == "__main__":
    main()
