from sender import Sender
from receiver import Receiver
from attacker import Attacker
import matplotlib.pyplot as plt

methods = ["none", "nonce", "counter", "hybrid"]
results = {}

for method in methods:

    sender = Sender()
    receiver = Receiver(method)
    attacker = Attacker()

    total = 0
    detected = 0

    for i in range(100):

        # Normal communication
        msg1 = sender.generate_message("UNLOCK")
        receiver.validate(msg1)

        msg2 = sender.generate_message("LOCK")
        receiver.validate(msg2)

        attacker.capture(msg1)
        attacker.capture(msg2)

        # -------- ATTACK 1: DELAYED REPLAY AFTER RESET --------
        receiver.reset()

        replay_old = msg1
        total += 1
        if not receiver.validate(replay_old):
            detected += 1

        # -------- ATTACK 2: OUT OF ORDER --------
        replay_wrong = msg1
        total += 1
        if not receiver.validate(replay_wrong):
            detected += 1

        # -------- ATTACK 3: MULTIPLE REPLAY --------
        for _ in range(2):
            total += 1
            if not receiver.validate(msg2):
                detected += 1

        # -------- ATTACK 4: COUNTER SKIP --------
        fake_msg = {
            "command": "UNLOCK",
            "nonce": msg1["nonce"],
            "counter": msg1["counter"] + 5
        }

        total += 1
        if not receiver.validate(fake_msg):
            detected += 1

    results[method] = detected / total

# -------- PRINT RESULTS --------
print("\nFinal Results:")
for k, v in results.items():
    print(f"{k}: {v:.2f}")

# -------- GRAPH --------
methods_list = list(results.keys())
values = list(results.values())

plt.figure()
bars = plt.bar(methods_list, values)

# Add values on top
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height,
             f"{height:.2f}", ha='center', va='bottom')

plt.title("Replay Attack Detection (Advanced Scenarios)")
plt.xlabel("Method")
plt.ylabel("Detection Rate")

plt.savefig("results/detection_rate.png")
plt.show()