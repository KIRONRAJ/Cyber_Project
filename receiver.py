class Receiver:
    def __init__(self, mode):
        self.mode = mode
        self.used_nonces = set()
        self.last_counter = 0

    def reset(self):
        # simulate device reset which clears nonce history and resets counter
        self.used_nonces.clear()
        self.last_counter = 0

    def validate(self, message):
        nonce = message["nonce"]
        counter = message["counter"]

        if self.mode == "none":
            return True

        if self.mode == "nonce":
            if nonce in self.used_nonces:
                return False
            self.used_nonces.add(nonce)
            return True

        if self.mode == "counter":
            if counter <= self.last_counter:
                return False
            self.last_counter = counter
            return True

        if self.mode == "hybrid":
            if nonce in self.used_nonces:
                return False
            if counter <= self.last_counter:
                return False
            self.used_nonces.add(nonce)
            self.last_counter = counter
            return True