#!/bin/python3

import pygame
import sys

# 初始化 Pygame
pygame.init()

# 创建一个窗口
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Pygame Mouse Input")

# 设置颜色
white = (255, 255, 255)
red = (255, 0, 0)

pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

# 主循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            # 鼠标移动事件处理
            mouse_x, mouse_y = event.pos
            print(f"Mouse position: ({mouse_x}, {mouse_y})")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 鼠标按下事件处理
            if event.button == 1:  # 左键
                print("Left mouse button pressed")
        elif event.type == pygame.MOUSEBUTTONUP:
            # 鼠标释放事件处理
            if event.button == 1:  # 左键
                print("Left mouse button released")

    # 在这里进行其他的游戏逻辑和渲染
    window.fill(white)

    # 绘制一个矩形，当鼠标悬停在上面时变为红色
    rect = pygame.Rect(100, 100, 200, 150)
    if rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(window, red, rect)
    else:
        pygame.draw.rect(window, red, rect, 2)

    pygame.display.flip()

