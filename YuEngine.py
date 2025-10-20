import os
import sys

from engine import main as engine
from tools import Cheek
from engine.core import game_object as GameObject

s = Cheek.check_compilation_status()

if not s['is_compiled'] == True:
    #如果在save/acc/中没有找到acc.txt，说明未登录，则跳转到登录界面
    if not os.path.exists('save/acc/acc.txt'):
        os.system('Login.exe')
        if not os.path.exists('save/acc/acc.txt'):
            sys.exit()
        else:
        #如果在save/acc/中找到acc.txt，说明已登录，则跳转到游戏界面
            game = engine.engine((800,600),60,"YuEngine")
    else:
        game = engine.engine((800,600),60,"YuEngine")






