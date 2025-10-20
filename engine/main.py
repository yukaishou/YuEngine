import pygame
import sys
from engine.core import scene
from engine.core import script
from prefabs.script import player_controller as ts
from engine import sdk
from engine.key import key
from engine import log
from engine import application

pygame.init()
class engine:
    def __init__(self, size, fps, tliie,scene_config,res):
        self.size = size
        self.res = res
        self.application = application.Application(self)
        self.log = log.Log()
        self.scene = scene.Scene(scene_config["file"],scene_config["dir"],self.log,self.res)
        self.running = True
        self.log.add_log("Initializing engine...","INFO")
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption(tliie)
        self.core = pygame
        self.log.add_log("Setting up screen...","INFO")
        self.clock = pygame.time.Clock()
        self.log.add_log("Setting up clock...","INFO")
        self.key = key.Key()
        self.log.add_log("Setting up key...","INFO")
        self.script_runner = script.ScriptRunner(self)
        self.log.add_log("Setting up script runner...","INFO")
        self.sdk = sdk.SDK(self,self.scene,self.key,None,self.core,self.application)
        self.log.add_log("Setting up SDK...","INFO")
        self.clock.tick(fps)
        self.subsystems = {
            "core": self.core,
            "scene": self.scene,
            "key": self.key,
            "script_runner": self.script_runner,
            "sdk": self.sdk,
            "log": self.log,
            "application": self.application,
        }
        while self.running:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.quit()
            except Exception as e:
                self.log.add_log(f"Error: {e}","ERROR")
            self.application.updeta()
            self.scene.draw(self.screen)
            for i in self.scene.game_objects:
                i.update()
            pygame.display.update()


    def quit(self):
        self.running = False
        self.log.add_log("Exiting...","INFO")
        self.log.save_log()
        sys.exit()

    def full_screen(self):
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)

    def windowed_screen(self,size):
        self.screen = pygame.display.set_mode(size)


