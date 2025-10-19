class PrefabScript():
    def __init__(self,sdk):
        self.engine = sdk
        self.core = sdk.core

    def start(self):
        self.player = self.engine.scene.game_objects[0]

    def update(self):
        self.key = self.engine.key.get_key()
        if self.key == self.core.K_w:
            self.player.rect.y -= 1
            print("w")
        if self.key == self.core.K_s:
            self.player.rect.y += 1
            print("s")
        if self.key == self.core.K_a:
            self.player.rect.x -= 1
            print("a")
        if self.key == self.core.K_d:
            self.player.rect.x += 1
            print("d")

