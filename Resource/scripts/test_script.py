class PrefabScript():
    def __init__(self,sdk):
        self.engine = sdk

    def start(self):
        self.engine.engine.log.add_log("started")

    def update(self):
        pass
