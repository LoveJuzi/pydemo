#!/bin/python3

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


class Camera:
    def __init__(self):
        self._pos = glm.vec3(0, 0, 3)
        self._front = glm.vec3(0, 0, -1)
        self._up = glm.vec3(0, 1, 0)

    def pos(self): return self._pos

    def setPos(self, pos):  self._pos = pos

    def front(self): return self._front

    def setFront(self, front): self._front = front

    def up(self): return self._up

    def setUp(self, up): self._up = up

    def view(self):
        return glm.lookAt(self._pos, self._pos + self._front, self._up)


def getCubePositions():
    return [glm.vec3(0.0,  0.0,  0.0),
            glm.vec3(2.0,  5.0, -15.0),
            glm.vec3(-1.5, -2.2, -2.5),
            glm.vec3(-3.8, -2.0, -12.3),
            glm.vec3(2.4, -0.4, -3.5),
            glm.vec3(-1.7,  3.0, -7.5),
            glm.vec3(1.3, -2.0, -2.5),
            glm.vec3(1.5,  2.0, -2.5),
            glm.vec3(1.5,  0.2, -1.5),
            glm.vec3(-1.3,  1.0, -1.5)]


def getData():
    return np.array([
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


class GameParam:
    def __init__(self, screenWidth, screenHeight):
        self._camera = Camera()
        self._deltaTime = 0.0
        self._lastTime = pygame.time.get_ticks() / 1000.0

        self._projection = glm.perspective(
            glm.radians(45.0), screenWidth/screenHeight, 0.1, 100)

    def camera(self): return self._camera

    def cameraSpeed(self): return 2.5 * self.deltaTime()

    def deltaTime(self): return self._deltaTime

    def setDeltaTime(self, deltaTime): self._deltaTime = deltaTime

    def lastTime(self): return self._lastTime

    def setLastTime(self, lastTime): self._lastTime = lastTime

    def projection(self): return self._projection


def processInput(gameParam):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

    camera = gameParam.camera()
    cameraSpeed = gameParam.cameraSpeed()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        camera.setPos(camera.pos() + cameraSpeed * camera.front())
    if keys[pygame.K_s]:
        camera.setPos(camera.pos() - cameraSpeed * camera.front())
    if keys[pygame.K_a]:
        camera.setPos(camera.pos() - cameraSpeed *
                      glm.normalize(glm.cross(camera.front(), camera.up())))
    if keys[pygame.K_d]:
        camera.setPos(camera.pos() + cameraSpeed *
                      glm.normalize(glm.cross(camera.front(), camera.up())))

    return True


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    data = getData()

    VAO = gl.glGenVertexArrays(1)
    gl.glBindVertexArray(VAO)

    VBO = gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VBO)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, data.nbytes, data, gl.GL_STATIC_DRAW)

    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE,
                             5 * ctypes.sizeof(ctypes.c_float),
                             ctypes.c_void_p(0))
    gl.glEnableVertexAttribArray(0)
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

    gl.glEnable(gl.GL_DEPTH_TEST)

    clock = pygame.time.Clock()

    cubePositions = getCubePositions()

    gameParam = GameParam(display[0], display[1])

    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    while True:
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

        gameParam.setDeltaTime(
            pygame.time.get_ticks() / 1000.0 - gameParam.lastTime())
        gameParam.setLastTime(gameParam.lastTime() + gameParam.deltaTime())

        if not processInput(gameParam):
            break

        gl.glClearColor(0.2, 0.3, 0.3, 1.0)
        gl.glClear(int(gl.GL_COLOR_BUFFER_BIT) | int(gl.GL_DEPTH_BUFFER_BIT))

        shader.use()

        shader.setMat4("view", gameParam.camera().view())
        shader.setMat4("projection", gameParam.projection())

        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, texture1)
        gl.glActiveTexture(gl.GL_TEXTURE1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, texture2)

        gl.glBindVertexArray(VAO)

        for index, cubePos in enumerate(cubePositions):
            model = glm.mat4()
            model = glm.translate(model, cubePos)
            angle = 20.0 * index
            model = glm.rotate(model, glm.radians(
                angle), glm.vec3(1, 0.3, 0.5))
            shader.setMat4("model", model)
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, data.size)

        gl.glBindVertexArray(0)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
