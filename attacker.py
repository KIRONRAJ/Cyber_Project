class Attacker:
    def __init__(self):
        self.memory = []

    def capture(self, message):
        self.memory.append(message)

    def get_old(self):
        if len(self.memory) > 1:
            return self.memory[0]
        return self.memory[-1]

    def get_latest(self):
        return self.memory[-1]

    def get_out_of_order(self):
        if len(self.memory) > 2:
            return self.memory[1]
        return self.memory[-1]