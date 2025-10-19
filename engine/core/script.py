import pygame

class ScriptRunner:
    def __init__(self, game_state):
        self.game_state = game_state

    def run_scripts(self, script):
        script.start()
