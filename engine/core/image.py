import pygame

class Image:
    def __init__(self, path,logger):
        self.image = pygame.image.load(path).convert()
        self.logger = logger
        self.logger.add_log("Image loaded: " + path, "INFO")
    def get_image(self):
        return self.image

    def set_image(self, image):
        self.image = image

    def draw(self, surface, x, y):
        surface.blit(self.image, (x, y))