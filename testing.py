import matplotlib.pyplot as plt
import numpy as np

from orbital_mechanics.orbits.elliptic import EllipticOrbit


orbit = EllipticOrbit(reference_true_anomaly_rad=np.pi / 2, eccentricity=0.5, omega_rad=np.pi / 3)

t_s = np.linspace(0, 3600 * 24, 13)
trajectory = orbit.trajectory(t_s=t_s)
trace = orbit.trace()

fig, ax = plt.subplots(figsize=(5, 5))
ax.plot(trace.x, trace.y, c="C0")
alpha = (t_s[-1] - t_s) / (t_s[-1] - t_s[0])
ax.scatter(trajectory.x, trajectory.y, c="C0", alpha=alpha)
ax.scatter([0], [0], s=20, c="black")
ax.axis("equal")
plt.show()
