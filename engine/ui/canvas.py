import pygame

class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.W_ui = []

    def clear(self, color):
        self.surface.fill(color)

    def draw (self,surface):
        for i in self.W_ui:
            surface.blit(surface, i.pos)

