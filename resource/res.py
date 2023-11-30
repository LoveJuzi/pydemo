#!/bin/python3

from PIL import Image
import OpenGL.GL as gl
import os


class Resource:
    def __init__(self):
        self._resourceDir = os.path.dirname(os.path.abspath(__file__))

    def resourceDir(self):
        return self._resourceDir

    def resourceFile(self, fileName):
        return os.path.abspath(self.resourceDir() + "/" + fileName)


resource = Resource()


def resourceFile(fileName):
    return resource.resourceFile(fileName)


def loadTexture(picturePath):
    texture = gl.glGenTextures(1)

    gl.glBindTexture(gl.GL_TEXTURE_2D, texture)

    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
    gl.glTexParameteri(gl.GL_TEXTURE_2D,
                       gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR_MIPMAP_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_2D,
                       gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)

    img = Image.open(picturePath)
    if (img.format == "PNG"):
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, img.width,
                        img.height, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, img.tobytes())
    else:
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, img.width,
                        img.height, 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, img.tobytes())
    gl.glGenerateMipmap(gl.GL_TEXTURE_2D)

    gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
    return texture
