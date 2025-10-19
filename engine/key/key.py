import pygame
class Key:
    def __init__(self):
        self.keys = {}

    def get_key(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return event.key
        return None

    def get_input(self):
        return pygame.key.get_pressed()