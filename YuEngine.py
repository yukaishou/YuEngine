from engine import main as engine
from tools import Cheek
import json

s = Cheek.check_compilation_status()
config = json.load(open("config.json"))
scene = {
    "file": config["scene"],
    "dir": config["scene_dir"]
}
if __name__ == "__main__":
    game = engine.engine((800,600),60,config["name"],scene,config["res"])






