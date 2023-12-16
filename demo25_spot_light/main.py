#!/bin/python3

from camera import Camera, CameraMovement
from pygame.locals import DOUBLEBUF
from pygame.locals import OPENGL
from res import resourceFile, loadTexture
from shader import Shader
import ctypes
import glm
import numpy as np
import OpenGL.GL as gl
import pygame


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
        -0.5, -0.5, -0.5,  0.0,  0.0, -1.0,  0.0, 0.0,
        0.5, -0.5, -0.5,  0.0,  0.0, -1.0,  1.0, 0.0,
        0.5,  0.5, -0.5,  0.0,  0.0, -1.0,  1.0, 1.0,
        0.5,  0.5, -0.5,  0.0,  0.0, -1.0,  1.0, 1.0,
        -0.5,  0.5, -0.5,  0.0,  0.0, -1.0,  0.0, 1.0,
        -0.5, -0.5, -0.5,  0.0,  0.0, -1.0,  0.0, 0.0,

        -0.5, -0.5,  0.5,  0.0,  0.0, 1.0,   0.0, 0.0,
        0.5, -0.5,  0.5,  0.0,  0.0, 1.0,   1.0, 0.0,
        0.5,  0.5,  0.5,  0.0,  0.0, 1.0,   1.0, 1.0,
        0.5,  0.5,  0.5,  0.0,  0.0, 1.0,   1.0, 1.0,
        -0.5,  0.5,  0.5,  0.0,  0.0, 1.0,   0.0, 1.0,
        -0.5, -0.5,  0.5,  0.0,  0.0, 1.0,   0.0, 0.0,

        -0.5,  0.5,  0.5, -1.0,  0.0,  0.0,  1.0, 0.0,
        -0.5,  0.5, -0.5, -1.0,  0.0,  0.0,  1.0, 1.0,
        -0.5, -0.5, -0.5, -1.0,  0.0,  0.0,  0.0, 1.0,
        -0.5, -0.5, -0.5, -1.0,  0.0,  0.0,  0.0, 1.0,
        -0.5, -0.5,  0.5, -1.0,  0.0,  0.0,  0.0, 0.0,
        -0.5,  0.5,  0.5, -1.0,  0.0,  0.0,  1.0, 0.0,

        0.5,  0.5,  0.5,  1.0,  0.0,  0.0,  1.0, 0.0,
        0.5,  0.5, -0.5,  1.0,  0.0,  0.0,  1.0, 1.0,
        0.5, -0.5, -0.5,  1.0,  0.0,  0.0,  0.0, 1.0,
        0.5, -0.5, -0.5,  1.0,  0.0,  0.0,  0.0, 1.0,
        0.5, -0.5,  0.5,  1.0,  0.0,  0.0,  0.0, 0.0,
        0.5,  0.5,  0.5,  1.0,  0.0,  0.0,  1.0, 0.0,

        -0.5, -0.5, -0.5,  0.0, -1.0,  0.0,  0.0, 1.0,
        0.5, -0.5, -0.5,  0.0, -1.0,  0.0,  1.0, 1.0,
        0.5, -0.5,  0.5,  0.0, -1.0,  0.0,  1.0, 0.0,
        0.5, -0.5,  0.5,  0.0, -1.0,  0.0,  1.0, 0.0,
        -0.5, -0.5,  0.5,  0.0, -1.0,  0.0,  0.0, 0.0,
        -0.5, -0.5, -0.5,  0.0, -1.0,  0.0,  0.0, 1.0,

        -0.5,  0.5, -0.5,  0.0,  1.0,  0.0,  0.0, 1.0,
        0.5,  0.5, -0.5,  0.0,  1.0,  0.0,  1.0, 1.0,
        0.5,  0.5,  0.5,  0.0,  1.0,  0.0,  1.0, 0.0,
        0.5,  0.5,  0.5,  0.0,  1.0,  0.0,  1.0, 0.0,
        -0.5,  0.5,  0.5,  0.0,  1.0,  0.0,  0.0, 0.0,
        -0.5,  0.5, -0.5,  0.0,  1.0,  0.0,  0.0, 1.0
    ], dtype=np.float32)


class GameParam:
    def __init__(self, screenWidth, screenHeight):
        self._camera = Camera()
        self._deltaTime = 0.0
        self._lastTime = pygame.time.get_ticks() / 1000.0

        self._projection = glm.perspective(
            glm.radians(45.0), screenWidth/screenHeight, 0.1, 100)

        self._centerPos = (screenWidth/2.0, screenHeight/2.0)

    def camera(self): return self._camera

    def deltaTime(self): return self._deltaTime

    def setDeltaTime(self, deltaTime): self._deltaTime = deltaTime

    def lastTime(self): return self._lastTime

    def setLastTime(self, lastTime): self._lastTime = lastTime

    def projection(self): return self._projection

    def getCenterPos(self): return self._centerPos


def processInput(gameParam):
    camera = gameParam.camera()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.MOUSEMOTION:
            xoffset = event.pos[0] - gameParam.getCenterPos()[0]
            yoffset = event.pos[1] - gameParam.getCenterPos()[1]
            pygame.mouse.set_pos(gameParam.getCenterPos())
            camera.processMouseMovment(xoffset, yoffset)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        camera.processKeyborad(CameraMovement.FORWARD, gameParam.deltaTime())
    if keys[pygame.K_s]:
        camera.processKeyborad(CameraMovement.BACKWARD, gameParam.deltaTime())
    if keys[pygame.K_a]:
        camera.processKeyborad(CameraMovement.LEFT, gameParam.deltaTime())
    if keys[pygame.K_d]:
        camera.processKeyborad(CameraMovement.RIGHT, gameParam.deltaTime())

    return True


def buildCubeVBO(data):
    VBO = gl.glGenBuffers(1)

    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VBO)

    gl.glBufferData(gl.GL_ARRAY_BUFFER, data.nbytes, data, gl.GL_STATIC_DRAW)

    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

    return VBO


def buildCubeVAO(VBO):
    VAO = gl.glGenVertexArrays(1)

    gl.glBindVertexArray(VAO)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VBO)

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
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

    return VAO


def buildLightVAO(VBO):
    VAO = gl.glGenVertexArrays(1)

    gl.glBindVertexArray(VAO)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VBO)

    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE,
                             8 * ctypes.sizeof(ctypes.c_float),
                             ctypes.c_void_p(0))
    gl.glEnableVertexAttribArray(0)

    gl.glBindVertexArray(0)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

    return VAO


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    data = getData()

    VBO = buildCubeVBO(data)

    cubeVAO = buildCubeVAO(VBO)

    lightVAO = buildLightVAO(VBO)

    lightColor = glm.vec3(1.0, 1.0, 1.0)

    diffuseMap = loadTexture(resourceFile("container2.png"))
    specularMap = loadTexture(resourceFile("container2_specular.png"))

    lightShader = Shader().init(resourceFile("shader18_light.vs"),
                                resourceFile("shader18_light.fs"))

    objectShader = Shader().init(resourceFile("shader21_obj.vs"),
                                 resourceFile("shader25_obj.fs"))

    gl.glEnable(gl.GL_DEPTH_TEST)

    clock = pygame.time.Clock()

    objectPos = glm.vec3(0, 0, 0)

    lightPos = glm.vec3(1.2, 1, 2)

    # lightDirection = glm.vec3(-0.2, -1, -0.3)

    objectModel = glm.translate(glm.mat4(1), objectPos)

    lightModel = glm.translate(glm.mat4(1), lightPos)
    lightModel = glm.scale(lightModel, glm.vec3(0.2))

    gameParam = GameParam(display[0], display[1])

    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    cubePositions = getCubePositions()

    while True:
        gameParam.setDeltaTime(
            pygame.time.get_ticks() / 1000.0 - gameParam.lastTime())
        gameParam.setLastTime(gameParam.lastTime() + gameParam.deltaTime())

        if not processInput(gameParam):
            break

        gl.glClearColor(0.1, 0.1, 0.1, 1.0)
        gl.glClear(int(gl.GL_COLOR_BUFFER_BIT) | int(gl.GL_DEPTH_BUFFER_BIT))

        lightShader.use()

        lightShader.setMat4("model", lightModel)
        lightShader.setMat4("view", gameParam.camera().view())
        lightShader.setMat4("projection", gameParam.projection())

        gl.glBindVertexArray(lightVAO)
        #gl.glDrawArrays(gl.GL_TRIANGLES, 0, data.size)

        objectShader.use()

        objectShader.setInt("material.diffuse", 0)
        objectShader.setInt("material.specular", 1)
        objectShader.setFloat("material.shiniess", 32.0)

        #objectShader.setVec3v("light.position", lightPos)
        # objectShader.setVec3v("light.direction", lightDirection)
        objectShader.setVec3v("light.position", gameParam.camera().pos())
        objectShader.setVec3v("light.direction", gameParam.camera().front())
        objectShader.setFloat("light.cutOff", glm.cos(glm.radians(12.5)))
        objectShader.setFloat("light.outerCutOff", glm.cos(glm.radians(17.5)))
        objectShader.setVec3v("light.ambient", 0.2 * lightColor)
        objectShader.setVec3v("light.diffuse", 0.5 * lightColor)
        objectShader.setVec3v("light.specular", lightColor)

        objectShader.setVec3v("viewPos", gameParam.camera().pos())

        objectShader.setMat4("model", objectModel)
        objectShader.setMat4("view", gameParam.camera().view())
        objectShader.setMat4("projection", gameParam.projection())

        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, diffuseMap)
        gl.glActiveTexture(gl.GL_TEXTURE1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, specularMap)

        gl.glBindVertexArray(cubeVAO)
        for index, cubePos in enumerate(cubePositions):
            model = glm.mat4()
            model = glm.translate(model, cubePos)
            angle = 20.0 * index
            model = glm.rotate(model,
                               glm.radians(angle),
                               glm.vec3(1, 0.3, 0.5))
            objectShader.setMat4("model", model)
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, data.size)

        gl.glBindVertexArray(0)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
