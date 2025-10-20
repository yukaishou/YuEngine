import os
import sys

from engine import main as engine
from tools import Cheek
from engine.core import game_object as GameObject

s = Cheek.check_compilation_status()

if __name__ == "__main__":
    game = engine.engine((800,600),60,"YuEngine")






