from datetime import datetime
class Log:
    def __init__(self):
        self.logs = []

    def add_log(self, log ,Type):
        log = "[" + Type + "] " + log
        self.logs.append(log)
        print(log)

    def get_logs(self):
        return self.logs.copy()

    def save_log(self):
        time = datetime.now()
        with open("../YuEngine/Log/" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".txt", "w") as f:
            for line in self.logs:
                f.write(line + "\n")
