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
from engine.ui import ui_text
from engine.ui import ui_button
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
            #self.img_cls.draw(self.screen,0,0, )
            #self.img_cls1.draw(self.screen,size[0]//2,size[1]//2 - 150)
            self.scene.draw(self.screen)
            for i in self.scene.game_objects:
                i.update()
            #self.txt.draw(self.screen)
            #self.bt.draw(self.screen)
            #self.bt1.draw(self.screen)
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

    def test_prefab(self):
        self.ts = ts.PrefabScript(self.sdk)
        self.m = m.PrefabScript(self.sdk)
        #self.obj1 = game_object.GameObject(0, 0, 25, 25, (255, 255, 255), [self.ts], self.log)
        self.obj2 = game_object.GameObject(0,0, self.size[0], 50, (18, 18, 18), [], self.log)
        #self.scene.add_game_object(self.obj1)
        self.scene.add_game_object(self.obj2)
        self.img_cls = im.Image("Resource\image\Luanch.jpg",self.log)
        self.img_cls1 = im.Image("Resource\image\editor\Asset/Texture.png",self.log)
        self.scene.play_sound("Resource/sound/Looby_B.mp3")
        self.bt = ui_button.Button(10,self.size[1] - 50, 200,40, "退出游戏", lambda: self.quit())
        self.bt1 = ui_button.Button(10, self.size[1] - 100, 200, 40, "开始游戏", lambda: print("开始游戏"))
        self.txt = ui_text.UIText("游戏大厅", (255, 255, 255), 10,10)
