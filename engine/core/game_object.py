import pygame

class GameObject:
    def __init__(self, x, y, width, height, color , scripts,logger):
        self.name = "GameObject"
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
        if self.scripts:
            for i in self.scripts:
                if i == None:
                    self.logger.add_log("script is None","ERROR")
                else:
                    print("123333123")
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
        if self.scripts == None:
            for i in self.scripts:
                if i == None:
                    self.logger.add_log("script is None","ERROR")
                    continue
                else:
                    i.update()
