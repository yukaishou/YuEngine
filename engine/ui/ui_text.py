import pygame

class UIText:
    def __init__(self, text, color, x, y):
        self.text = text
        self.font = pygame.font.Font("../YuEngine\Resource/font\simhei.ttf", 24)
        self.color = color
        self.x = x
        self.y = y

    def draw(self, surface):
        text_surface = self.font.render(self.text, True, self.color)
        surface.blit(text_surface, (self.x, self.y))