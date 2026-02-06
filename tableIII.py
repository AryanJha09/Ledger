import matplotlib.pyplot as plt
import numpy as np

# Case types and assumption proportions (from your paper)
case_types = ["Normal", "Missing", "Contradictory", "Stress", "No-uncertainty"]
benign = np.array([87.5, 84.8, 50.0, 72.5, 0.0])
escalated = np.array([12.5, 15.2, 50.0, 27.5, 0.0])
degenerate = np.array([0.0, 0.0, 0.0, 0.0, 0.0])

x = np.arange(len(case_types))

plt.figure(figsize=(6, 3.5))
plt.bar(x, benign, label="Benign")
plt.bar(x, escalated, bottom=benign, label="Escalated")
plt.bar(x, degenerate, bottom=benign+escalated, label="Degenerate")

plt.xticks(x, case_types, rotation=20)
plt.ylabel("Proportion (%)")
plt.legend(frameon=False)
plt.tight_layout()

plt.savefig("assumption_severity_by_case.png", dpi=300)
plt.close()
