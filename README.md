# Single file

# **Replay Attack Detection System (Hybrid Framework)**

---
![Replay Attack Detection System Diagram](/diagram.png)
---

## **1. sender.py**

### 🔹 Logic

The sender simulates a **key fob (remote control)** in a smart car system.

Its job is to:

- Generate a command (e.g., UNLOCK)
- Generate a random nonce
- Maintain a counter (sequence number)

Each message must be:

- Unique → using nonce
- Ordered → using counter

---

### 🔹 Explanation

- Counter increases every time a message is sent
- Nonce is random and different every time

Example:

| Message | Nonce | Counter |
| --- | --- | --- |
| UNLOCK | 834729 | 1 |
| LOCK | 192847 | 2 |

---

### 🔹 Code

```python
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
```

---

## **2. receiver.py**

### 🔹 Logic

The receiver simulates the **car system**.

Its job is to:

- Check if message is fresh (nonce)
- Check if message is in correct order (counter)
- Accept or reject message

---

### 🔹 Correct Understanding

```python
if counter <= self.last_counter:
    return False
```

---

### 🔹 What is `last_counter`?

👉 It stores the last valid counter value accepted

Example:

```
Last accepted = 5
```

---

### 🔹 What is this checking?

👉 “Is this message old or reused?”

---

### 🔹 Logic Table

| Incoming Counter | Result | Reason |
| --- | --- | --- |
| 6 | ✅ Accept | New message |
| 5 | ❌ Reject | Duplicate |
| 4 | ❌ Reject | Old message |
| 3 | ❌ Reject | Old message |

---

### 🔹 What is NONCE doing?

👉 Prevents reuse of same message

| Nonce Seen Before? | Result |
| --- | --- |
| No | ✅ Accept |
| Yes | ❌ Reject |

---

### 🔹 Reset Function

```python
def reset(self):
```

👉 Simulates:

- Device restart
- Loss of memory

This is important because:

- Real IoT devices may reboot
- Security memory may reset

---

### 🔹 Code

```python
class Receiver:
    def __init__(self, mode):
        self.mode = mode
        self.used_nonces = set()
        self.last_counter = 0

    def reset(self):
        # simulate device reset
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
```

---

## **3. attacker.py**

### 🔹 Logic

The attacker simulates a hacker.

Its job is to:

- Capture messages
- Store them
- Replay them later

---

### 🔹 Types of Attacks

| Attack | Description |
| --- | --- |
| Old replay | Reuse old message |
| Multiple replay | Send same message repeatedly |
| Out-of-order | Send wrong sequence |

---

### 🔹 Code

```python
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
```

---

## **4. main.py**

### 🔹 Logic

This is the **main simulation controller**.

It:

1. Runs system with different methods:
    - none
    - nonce
    - counter
    - hybrid
2. Simulates attacks:
    - delayed replay
    - multiple replay
    - out-of-order
    - counter skip
3. Measures:
    - detection rate

---

### 🔹 What is Detection Rate?

👉 How many attacks were blocked

Formula:

```
Detection Rate = detected_attacks / total_attacks
```

---

### 🔹 Code

```python
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

        msg1 = sender.generate_message("UNLOCK")
        receiver.validate(msg1)

        msg2 = sender.generate_message("LOCK")
        receiver.validate(msg2)

        attacker.capture(msg1)
        attacker.capture(msg2)

        # Attack 1: Replay after reset
        receiver.reset()
        replay_old = msg1

        total += 1
        if not receiver.validate(replay_old):
            detected += 1

        # Attack 2: Out of order
        replay_wrong = msg1
        total += 1
        if not receiver.validate(replay_wrong):
            detected += 1

        # Attack 3: Multiple replay
        for _ in range(2):
            total += 1
            if not receiver.validate(msg2):
                detected += 1

        # Attack 4: Counter skip
        fake_msg = {
            "command": "UNLOCK",
            "nonce": msg1["nonce"],
            "counter": msg1["counter"] + 5
        }

        total += 1
        if not receiver.validate(fake_msg):
            detected += 1

    results[method] = detected / total

print("\nFinal Results:")
for k, v in results.items():
    print(f"{k}: {v:.2f}")
```

---

## **5. Graph Generation**

### 🔹 Logic

This creates a bar chart showing:

👉 Which method performs better

---

### 🔹 Code

```python
methods_list = list(results.keys())
values = list(results.values())

plt.figure()
bars = plt.bar(methods_list, values)

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height,
             f"{height:.2f}", ha='center', va='bottom')

plt.title("Replay Attack Detection (Advanced Scenarios)")
plt.xlabel("Method")
plt.ylabel("Detection Rate")

plt.savefig("results/detection_rate.png")
plt.show()
```

---

# 🔥 Output

Your system proves:

| Method | Weakness |
| --- | --- |
| nonce | fails when reset |
| counter | fails when desync |
| hybrid | handles both |

---

#
