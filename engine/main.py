import pygame
import sys
from engine.core import game_object, scene
from engine.core import script
from prefabs.script import player_controller as ts
from prefabs.script import cube_move as m
from engine import sdk
from engine.key import key
from engine import log
from engine import application
from engine.core import image as im
import time

pygame.init()
class engine:
    def __init__(self, size, fps, tliie):
        self.size = size
        self.application = application.Application(self)
        self.log = log.Log()
        self.scene = scene.Scene("prefabs/projects/prefab_project/assets/scene/scene/scene.json","prefabs/projects/prefab_project/assets/scene/scene/",self.log)
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
        #self.test_prefab()
        player_controller = ts.PrefabScript(self.sdk)
        player = self.scene.game_objects[0]
        player.scripts.append(player_controller)
        player_controller.start()
        img = im.Image("Resource/image/Cat.jpg",self.log)
        while self.running:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.quit()
                    #self.bt.handle_event(event)
                    #self.bt1.handle_event(event)
            except Exception as e:
                self.log.add_log(f"Error: {e}","ERROR")
            self.application.updeta()
            #self.img_cls1.draw(self.screen,size[0]//2,size[1]//2 - 150)
            self.scene.draw(self.screen)
            for i in self.scene.game_objects:
                i.update()
            #self.txt.draw(self.screen)
            #self.bt.draw(self.screen)
            #self.bt1.draw(self.screen)
            #img.draw(self.screen,size[0]//2,0, )
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


