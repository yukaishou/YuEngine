from engine import main as engine
from engine.core import game_object as GameObject
if __name__ == "__main__":
    game = engine.engine((800,600),60,"YuEngine")
    game.log.save_log()
else:
    game = engine.engine((800,600),60,"YuEngine")
    game.log.save_log()
