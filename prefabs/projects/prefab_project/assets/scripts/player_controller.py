class PrefabScript():
    def __init__(self,sdk):
        self.engine = sdk
        self.core = sdk.core
        self.public_vars = {
            "speed": 1
        }

    def start(self):
        self.player = self.engine.scene.game_objects[0]
        self.engine.engine.log.add_log("PlayerController script started", "INFO")

    def update(self):
        self.key = self.engine.key.get_input()
        if self.key[self.core.K_w]:
            self.player.rect.y -= self.public_vars["speed"]

        if self.key[self.core.K_s]:
            self.player.rect.y += self.public_vars["speed"]

        if self.key[self.core.K_a]:
            self.player.rect.x -= self.public_vars["speed"]

        if self.key[self.core.K_d]:
            self.player.rect.x += self.public_vars["speed"]

        if self.key[self.core.K_SPACE]:
            self.engine.application.quit()

        if self.key[self.core.K_f]:
            self.engine.application.set_window_mode("fullscreen")

        if self.key[self.core.K_g]:
            self.engine.application.set_window_mode("windowed")

