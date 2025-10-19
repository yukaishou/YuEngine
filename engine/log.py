class Log:
    def __init__(self):
        self.logs = []

    def add_log(self, log ,Type):
        log = "[" + Type + "] " + log
        self.logs.append(log)
        print(log)

    def get_logs(self):
        return self.logs

    def save_log(self,time):
        self.log = self.logs
        with open("../Yuengine/Log/" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".txt", "w") as f:
            for line in self.log:
                f.write(line + "\n")
