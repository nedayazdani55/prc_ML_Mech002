# generate_dataset.py
import csv, os
import numpy as np
from truss_fea import build_demo_truss, solve_truss

OUT = "outputs/dataset.csv"
os.makedirs("outputs", exist_ok=True)

def sample_and_save(n_samples=200):
    with open(OUT, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["load","A","max_stress","max_disp"])
        for _ in range(n_samples):
            load = -np.random.uniform(200.0, 2000.0)
            A = 10**np.random.uniform(-6, -3)  # between 1e-6 and 1e-3
            nodes, elements, loads, fixed = build_demo_truss(load=load, A=A)
            res = solve_truss(nodes, elements, loads, fixed)
            writer.writerow([load, A, res["max_stress"], res["max_disp"]])

if __name__ == "__main__":
    sample_and_save(500)
    print("dataset saved to", OUT)
