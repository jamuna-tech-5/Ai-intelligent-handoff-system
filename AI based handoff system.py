import random
import time

print("\n===== AI-Based Intelligent Handoff System =====\n")

# -----------------------------
# SETTINGS
# -----------------------------
MAX_STEPS = 12        # number of simulation steps
THRESHOLD = 4         # minimum improvement needed to switch
COOLDOWN = 2          # wait time after switching (to save power)

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
        # simulate changes in signal, load, and distance
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
        # check if signal is decreasing
        if len(self.history) < 3:
            return False

        drop = self.history[-2] - self.history[-1]

        if drop > 6 or self.history[-1] < 40:
            return True
        return False

    def calculate_stability(self):
        if len(self.history) < 2:
            return 80
        diff = abs(self.history[-1] - self.history[-2])
        return max(40, 100 - diff * 2)

    def calculate_score(self, tower, stability):
        # scoring based on signal, load, distance, and stability
        score = (
            0.5 * tower.signal +
            0.3 * stability -
            0.3 * tower.load -
            0.2 * (tower.distance / 2)
        )
        return round(score, 2)

    def calculate_probabilities(self, scores):
        # convert scores into percentages
        min_score = min(scores)
        adjusted = [s - min_score + 1 for s in scores]
        total = sum(adjusted)
        probs = [(s / total) * 100 for s in adjusted]
        return [round(p, 1) for p in probs]

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
current_tower = towers[0]

# -----------------------------
# SIMULATION START
# -----------------------------
for step in range(1, MAX_STEPS + 1):

    print(f"\n----- TIME STEP {step} -----")

    # update environment
    for t in towers:
        t.update()

    # current signal
    signal = current_tower.signal
    engine.update_history(signal)

    print(f"Current Tower: {current_tower.name}")
    print(f"Signal: {round(signal,1)}")
    print(f"Signal History: {[round(x,1) for x in engine.history]}")

    stability = engine.calculate_stability()

    # check if problem is predicted
    if engine.predict_problem():
        print("\n⚠️ AI detected signal problem")

        print("\nEvaluating Towers:")
        scores = []

        for t in towers:
            s = engine.calculate_score(t, stability)
            scores.append(s)

            print(f"{t.name} -> Signal:{round(t.signal,1)} | Load:{t.load}% | Distance:{t.distance} | Score:{s}")

        # calculate probability
        probs = engine.calculate_probabilities(scores)

        print("\nSwitching Probability:")
        for i, t in enumerate(towers):
            print(f"{t.name} -> {probs[i]}%")

        # find best tower
        best_index = scores.index(max(scores))
        best_tower = towers[best_index]

        current_score = scores[towers.index(current_tower)]
        best_score = scores[best_index]

        print("\nDecision:")

        if best_tower != current_tower and best_score > current_score + THRESHOLD and engine.cooldown == 0:
            print(f"🚀 Switching from {current_tower.name} to {best_tower.name}")
            current_tower = best_tower
            engine.cooldown = COOLDOWN
        else:
            print("Staying on current tower (no strong reason to switch)")

    else:
        print("Network stable (no switching needed)")

    if engine.cooldown > 0:
        engine.cooldown -= 1

    time.sleep(1)

print("\n===== Simulation Finished =====")