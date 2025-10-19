import pygame

class Application:
    def __init__(self,engine):
        self.engine = engine
        self.clock = pygame.time.Clock()
        self.fps = 0
    def updeta(self):
        pass
    def quit(self):
        self.engine.quit()

    def set_window_mode(self,type):
        if type == "fullscreen":
            self.engine.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        elif type == "windowed":
            self.engine.screen = pygame.display.set_mode((self.engine.size[0],self.engine.size[1]))