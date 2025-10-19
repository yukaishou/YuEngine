import sys

import pygame
import os
import time

# 初始化Pygame
pygame.init()

# 设置窗口大小
width, height = 600,400

# 创建一个窗口
screen = pygame.display.set_mode((width, height), pygame.NOFRAME)  # 创建无边框窗口

# 设置窗口标题
pygame.display.set_caption('YuEngine')

# 循环标志
running = True

# 游戏循环
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # 按下ESC键退出
                running = False

    # 填充背景颜色
    screen.fill((0, 0, 0))  # 使用黑色填充
    #绘制图片
    fimg = pygame.image.load("Resource/image/luanch.jpg")  # 加载图片
    fimg_rect = fimg.get_rect()  # 获取图片的矩形
    fimg_rect.center = (width//2, height//2)  # 设置图片的位置
    screen.blit(fimg, fimg_rect)  # 绘制图片
    img = pygame.image.load("Resource/image/Logo.png")  # 加载图片
    img_rect = img.get_rect() #获取图片的矩形
    img_rect.center = (25 , height - 52.5)  # 设置图片的位置
    screen.blit(img, img_rect)  # 绘制图片
    # 绘制文字
    font = pygame.font.Font(None, 36)  # 设置字体和大小
    text = font.render('YuEngine', True, (255, 255, 255))  # 设置文字内容、是否加粗、颜色
    text_rect = text.get_rect()  # 获取文字的矩形
    text_rect.center = (100, height -50)
    screen.blit(text, text_rect)  # 绘制文字

    # 更新屏幕显示
    pygame.display.flip()
    # 延迟10毫秒
    time.sleep(7.5)

    # 关闭窗口
    running = False



# 退出Pygame
pygame.quit()
try:
    #打开Main_UI.py
    os.system("python Main_UI.py");sys.exit()
except:
    #打开Main_UI.exe
    os.system("Main_UI.exe");sys.exit()