#!/bin/python3

from enum import Enum, auto
import math
import glm

class CameraMovement(Enum):
    FORWARD = auto()
    BACKWARD = auto()
    LEFT = auto()
    RIGHT = auto()


class Camera:
    def __init__(self):
        self._pos = glm.vec3(0, 0, 3)
        self._front = glm.vec3(0, 0, -1)
        self._up = glm.vec3(0, 1, 0)
        self._right = glm.vec3()
        self._yaw = -90
        self._pitch = 0

        self.updateVectors()

    def sensitivity(self): return 0.05

    def movementSpeed(self): return 2.5

    def pos(self): return self._pos

    def setPos(self, pos):  self._pos = pos

    def front(self): return self._front

    def setFront(self, front): self._front = front

    def right(self): return self._right

    def setRight(self, right): self._right = right

    def up(self): return self._up

    def setUp(self, up): self._up = up

    def view(self):
        return glm.lookAt(self._pos, self._pos + self._front, self._up)

    def yaw(self): return self._yaw

    def pitch(self): return self._pitch

    def setYaw(self, yaw): self._yaw = yaw

    def setPitch(self, pitch, constrainPitch=True):
        if pitch > 89.0 and constrainPitch:
            self._pitch = 89.0
        elif pitch < -89.0 and constrainPitch:
            self._pitch = -89.0
        else:
            self._pitch = pitch

    def processKeyborad(self, direction: CameraMovement, deltaTime):
        velocity = self.movementSpeed() * deltaTime
        if direction == CameraMovement.FORWARD:
            self.setPos(self.pos() + self.front() * velocity)
        if direction == CameraMovement.BACKWARD:
            self.setPos(self.pos() - self.front() * velocity)
        if direction == CameraMovement.LEFT:
            self.setPos(self.pos() - self.right() * velocity)
        if direction == CameraMovement.RIGHT:
            self.setPos(self.pos() + self.right() * velocity)

    def processMouseMovment(self, xoffset, yoffset, constrainPitch=True):
        xoffset *= self.sensitivity()
        yoffset *= self.sensitivity()
        self.setYaw(self.yaw() + xoffset)
        self.setPitch(self.pitch() + yoffset, constrainPitch)

        self.updateVectors()

    def updateVectors(self):
        direction = glm.vec3()
        direction.x = math.cos(glm.radians(self.pitch())) * \
            math.cos(glm.radians(self.yaw()))
        direction.y = math.sin(glm.radians(self.pitch()))
        direction.z = math.cos(glm.radians(self.pitch())) * \
            math.sin(glm.radians(self.yaw()))

        self.setFront(glm.normalize(direction))
        self.setRight(glm.normalize(glm.cross(self.front(), self.up())))
        self.setUp(glm.normalize(glm.cross(self.right(), self.front())))

