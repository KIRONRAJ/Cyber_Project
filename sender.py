import random

class Sender:
    def __init__(self):
        self.counter = 0

    def generate_message(self, command):
        self.counter += 1
        nonce = random.randint(100000, 999999)

        return {
            "command": command,
            "nonce": nonce,
            "counter": self.counter
        }