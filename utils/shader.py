#!/bin/python3

import OpenGL.GL as gl
import glm


class Shader:
    def __init__(self):
        self._programId = None

    def init(self, vertexPath, fragmentPath):
        # 1. read code from path
        vertexCode = None
        with open(vertexPath, 'r', encoding='utf-8') as f:
            vertexCode = f.read()

        fragmentCode = None
        with open(fragmentPath, 'r', encoding='utf-8') as f:
            fragmentCode = f.read()

        # 2. create shader
        self._programId = _createShaderProgram(vertexCode, fragmentCode)

        return self

    def getProgramId(self):
        return self._programId

    def use(self):
        gl.glUseProgram(self.getProgramId())

    def setBool(self, name, val):
        gl.glUniform1i(gl.glGetUniformLocation(self.getProgramId(), name), val)

    def setInt(self, name, val):
        gl.glUniform1i(gl.glGetUniformLocation(self.getProgramId(), name), val)

    def setFloat(self, name, val):
        gl.glUniform1f(gl.glGetUniformLocation(self.getProgramId(), name), val)

    def setVec3v(self, name, val):
        gl.glUniform3fv(gl.glGetUniformLocation(self.getProgramId(), name), 1,
                        glm.value_ptr(val))

    def setVec3(self, name, x, y, z):
        gl.glUniform3f(gl.glGetUniformLocation(self.getProgramId(), name), x, y, z)

    def setMat4(self, name, val):
        gl.glUniformMatrix4fv(gl.glGetUniformLocation(self.getProgramId(), name),
                              1, gl.GL_FALSE,
                              glm.value_ptr(val))


def _compileShader(shaderType, source):
    shader = gl.glCreateShader(shaderType)
    gl.glShaderSource(shader, source)
    gl.glCompileShader(shader)

    if not gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS):
        raise RuntimeError(gl.glGetShaderInfoLog(shader))

    return shader


def _createShaderProgram(vertexSource, fragmentSource):
    vertexShader = _compileShader(gl.GL_VERTEX_SHADER, vertexSource)
    fragmentShader = _compileShader(gl.GL_FRAGMENT_SHADER, fragmentSource)

    shaderProgram = gl.glCreateProgram()
    gl.glAttachShader(shaderProgram, vertexShader)
    gl.glAttachShader(shaderProgram, fragmentShader)
    gl.glLinkProgram(shaderProgram)

    if not gl.glGetProgramiv(shaderProgram, gl.GL_LINK_STATUS):
        raise RuntimeError(gl.glGetProgramInfoLog(shaderProgram))

    gl.glDeleteShader(vertexShader)
    gl.glDeleteShader(fragmentShader)

    return shaderProgram
