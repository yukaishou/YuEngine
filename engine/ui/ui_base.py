import pygame

class UIBase:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 16)
        self.font_large = pygame.font.Font(None, 64)
        self.font_huge = pygame.font.Font(None, 128)
        self.font_color = (255, 255, 255)
        self.bg_color = (0, 0, 0)
        self.border_color = (255, 255, 255)
        self.border_width = 2
        self.padding = 10
        self.margin = 10
        self.width = 0
        self.height = 0
        self.x = 0
        self.y = 0
        self.visible = True