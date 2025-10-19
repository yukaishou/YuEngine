import pygame
from engine.core import sound
import json

class Scene:
    def __init__(self, path,dirpath,logger):
        self.logger = logger
        self.path = path
        self.game_objects = []
        self.camera = None
        self.background_color = (0, 0, 0)
        self.load_(path,dirpath)

    def add_game_object(self, game_object):
        self.game_objects.append(game_object)
        self.logger.add_log(f"GameObject added to scene", "INFO")
        game_object.start()


    def play_sound(self, sound_name):
        snd_tmp = sound.Sound(sound_name)
        snd_tmp.play()
        self.logger.add_log(f"Sound is played", "INFO")

    def load(self, path,dirpath):
        pass
    def load_(self, path,dirpath):
        with open(path, 'r') as file:
            self.main = json.load(file)
        self.info = SceneInfo(self.main["name"], self.main["game_objects"])
        self.dirpath = dirpath
        self.obj_info = []
        for i in self.info.game_objects:
            try:
                #获取当前GameObject的脚本的序列
                index =  i
                script_path = f"{self.dirpath}GameObjects_info/{i[index]['name']}/scripts.json"
                transform_path = f"{self.dirpath}GameObjects_info/{i[index]['name']}/transform.json"
                render_path = f"{self.dirpath}GameObjects_info/{i[index]['name']}/render.json"
                main_path = f"{self.dirpath}GameObjects_info/{i[index]['name']}/main.json"
            except:
                print(f"GameObject {self.main['name']} not found in scene")
                continue
            with open(script_path, 'r') as script_file, open(transform_path, 'r') as transform_file, \
                 open(render_path, 'r') as render_file, open(main_path, 'r') as main_file:
                scripts = json.load(script_file)
                transform = json.load(transform_file)
                render = json.load(render_file)
                main = json.load(main_file)

            self.obj_info.append(GameObjectInfo(i['name'], scripts, transform, render, main))
        print("Scene loaded info:")
        print("name:" + self.info.name)
        print("game_objects:")
        print(len(self.obj_info))

    def update(self):
        for game_object in self.game_objects:
            game_object.update()

    def draw(self, screen):
        screen.fill(self.background_color)
        for game_object in self.game_objects:
            game_object.draw(screen)

class SceneInfo:
    def __init__(self, name, game_objects):
        self.name = name
        self.game_objects = game_objects
        self.game_objects_name = []
        for i in game_objects:
            self.game_objects_name.append(i)
        print(self.game_objects_name)

class GameObjectInfo:
    def __init__(self, name, scripts, transform, render, main):
        self.name = name
        self.scripts = scripts
        self.transform = transform
        self.render = render
        self.main = main
