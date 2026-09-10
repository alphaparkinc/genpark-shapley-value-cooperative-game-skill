import sys
from client import ShapleyValueEngine

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

def run():
    print(">>> Demonstrating Shapley Value Computation...")
    players = ["A", "B", "C"]
    
    # Characteristic function: Any coalition with >= 2 members generates 100 profit
    def v(coalition):
        return 100.0 if len(coalition) >= 2 else 0.0

    engine = ShapleyValueEngine(players)
    values = engine.compute(v)
    print(f"Shapley Values: {values}")

    for p in players:
        assert abs(values[p] - 100.0 / 3.0) < 1e-4
    print("[PASS] Shapley Value Cooperative Game verified.")

if __name__ == "__main__":
    run()
