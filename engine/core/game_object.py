import pygame
from engine import core

class GameObject:
    def __init__(self, x, y, width, height, color , scripts,logger):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.scripts = scripts
        self.image = None
        self.logger = logger

    def start(self):
        for i in self.scripts:
            i.start()
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        try:
            if self.image:
                self.image.draw(screen, self.x, self.y)
        except:
            #self.logger.add_log("failed to drawing image","ERROR")
            pass


    def update(self):
        for i in self.scripts:
            i.update()