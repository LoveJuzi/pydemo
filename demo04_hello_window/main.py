#!/usr/bin/python3

import pygame
from pygame.locals import DOUBLEBUF
from pygame.locals import OPENGL
import OpenGL.GL as gl
import OpenGL.GLU as glu

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glu.gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    gl.glTranslatef(0.0, 0.0, -5)

    while True:
        processInput()

        gl.glClearColor(0.2, 0.3, 0.3, 1.0)
        gl.glClear(int(gl.GL_COLOR_BUFFER_BIT) | int(gl.GL_DEPTH_BUFFER_BIT))
        pygame.display.flip()
        pygame.time.wait(10)

def processInput():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # exit windown
            pygame.quit()
            quit()

if __name__ == "__main__":
    main()
