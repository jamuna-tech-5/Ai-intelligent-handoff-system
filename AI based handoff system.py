import random
import time

print("\n===== AI Intelligent Handoff System =====\n")

# -----------------------------
# SETTINGS
# -----------------------------
MAX_STEPS = 10        # total simulation steps
THRESHOLD = 5         # minimum improvement needed to switch
COOLDOWN_TIME = 2     # wait time after switching

# -----------------------------
# TOWER CLASS
# -----------------------------
class Tower:
    def __init__(self, name, base_signal, distance):
        self.name = name
        self.base_signal = base_signal
        self.distance = distance
        self.signal = base_signal
        self.load = random.randint(20, 70)

    def update(self):
        # simulate real-world changes
        self.signal = max(10, min(100, self.base_signal + random.uniform(-10, 10)))
        self.load = max(10, min(90, self.load + random.randint(-5, 5)))
        self.distance = max(10, min(200, self.distance + random.randint(-5, 5)))

# -----------------------------
# AI ENGINE
# -----------------------------
class AIEngine:
    def __init__(self):
        self.history = []
        self.cooldown = 0

    def update_history(self, signal):
        self.history.append(signal)
        if len(self.history) > 5:
            self.history.pop(0)

    def predict_problem(self):
        # detect signal drop
        if len(self.history) < 3:
            return False

        drop = self.history[-2] - self.history[-1]

        if drop > 5 or self.history[-1] < 40:
            return True
        return False

    def stability(self):
        if len(self.history) < 2:
            return 80
        diff = abs(self.history[-1] - self.history[-2])
        return max(40, 100 - diff * 2)

    def score(self, tower, stability):
        # higher score = better tower
        return round(
            (0.5 * tower.signal) +
            (0.3 * stability) -
            (0.3 * tower.load) -
            (0.2 * (tower.distance / 2)),
            2
        )

    def probability(self, scores):
        # convert scores to percentage
        min_score = min(scores)
        adjusted = [s - min_score + 1 for s in scores]
        total = sum(adjusted)
        return [round((s / total) * 100, 1) for s in adjusted]

# -----------------------------
# CREATE TOWERS
# -----------------------------
towers = [
    Tower("Tower A", 45, 120),
    Tower("Tower B", 70, 80),
    Tower("Tower C", 60, 60),
    Tower("Tower D", 40, 150)
]

engine = AIEngine()
current = towers[0]

# -----------------------------
# SIMULATION
# -----------------------------
for step in range(1, MAX_STEPS + 1):

    print(f"\n----- STEP {step} -----")

    # update towers
    for t in towers:
        t.update()

    # current signal
    signal = current.signal
    engine.update_history(signal)

    print(f"Current Tower: {current.name}")
    print(f"Signal: {round(signal,1)}")
    print(f"History: {[round(x,1) for x in engine.history]}")

    stab = engine.stability()

    # check if problem predicted
    if engine.predict_problem():

        print("\n⚠️ Signal problem predicted")

        print("\nEvaluating towers:")
        scores = []

        for t in towers:
            s = engine.score(t, stab)
            scores.append(s)

            print(f"{t.name} → Signal:{round(t.signal,1)}, Load:{t.load}%, Distance:{t.distance}, Score:{s}")

        probs = engine.probability(scores)

        print("\nProbability:")
        for i, t in enumerate(towers):
            print(f"{t.name} → {probs[i]}%")

        # find best tower
        best_index = scores.index(max(scores))
        best = towers[best_index]

        current_score = scores[towers.index(current)]
        best_score = scores[best_index]

        print("\nDecision:")

        if best != current and best_score > current_score + THRESHOLD and engine.cooldown == 0:
            print(f"🚀 Switching from {current.name} to {best.name}")
            current = best
            engine.cooldown = COOLDOWN_TIME
        else:
            print("Staying on current tower (no strong improvement)")

    else:
        print("Network stable")

    if engine.cooldown > 0:
        engine.cooldown -= 1

    time.sleep(1)

print("\n===== Simulation Complete =====")
print(f"Final Tower: {current.name}")
