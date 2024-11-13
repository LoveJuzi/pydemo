#!/usr/bin/python3

import numpy as np
import glm

# 创建一个4x4的矩阵
mat4 = np.array([
    [1.0, 0.0, 0.0, 0.0],
    [0.0, 1.0, 0.0, 0.0],
    [0.0, 0.0, 1.0, 0.0],
    [0.0, 0.0, 0.0, 1.0]
])

# 打印矩阵
print(mat4)

vec = glm.vec4(1.0, 0.0, 0.0, 1.0)
print(vec)

trans = glm.mat4()
trans = glm.translate(trans, glm.vec3(1, 1, 0))
print(trans)

vec = trans * vec
print(vec)

glm.scale(glm.mat4(), glm.vec3(0.5, 0.5, 0.5))
glm.rotate(glm.mat4(), glm.radians(90.0), glm.vec3(0, 0, 1))
