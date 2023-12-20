import numpy as np

from orbital_mechanics.constants import PI


def in_quadrant_one_or_two(theta: float) -> bool:
     if (theta % (2 * PI)) <= PI:
          return True
     else:
          return False


def adjust_quadrants_from_arccos(angles_solved, angles_original):
     if np.isscalar(angles_solved):
          return _adj_quadrants_from_arccos(angles_solved, angles_original)
     else:
          return _v_adj_quadrants_from_arccos(angles_solved, angles_original)


def _adj_quadrants_from_arccos(angles_solved: float, angles_original: float) -> float:
     if in_quadrant_one_or_two(angles_original):
          return angles_solved
     else:
          return PI + (PI - angles_solved)


def _v_adj_quadrants_from_arccos(angles_solved: np.ndarray, angles_original: np.ndarray) -> np.ndarray:
     mask = ((angles_original % (2 * PI)) > PI)
     angles_solved[mask] = PI + (PI - angles_solved[mask])
     return angles_solved


# Convert true anomaly to eccentric anomaly
def true_to_eccentric(nu: np.ndarray, e: float) -> np.ndarray:
     E = np.arccos((e + np.cos(nu)) / (1 + e * np.cos(nu)))
     return adjust_quadrants_from_arccos(E, nu)


# Convert eccentric anomaly to mean anomaly
def eccentric_to_mean(E: np.ndarray, e: float) -> np.ndarray:
     return E - e * np.sin(E)


# Directly converit true anomaly to mean anomaly
def true_to_mean(nu: np.ndarray, e: float) -> np.ndarray:
     return eccentric_to_mean(true_to_eccentric(nu, e), e)


# Convert eccentric anomaly to true anomaly
def eccentric_to_true(E: np.ndarray, e: float) -> np.ndarray:
     nu = np.arccos((np.cos(E) - e) / (1 - e * np.cos(E)))
     return adjust_quadrants_from_arccos(nu, E)


# Wrapper
def mean_to_eccentric(M, e, method="Newton-Raphson"):
     if np.isscalar(M):
          return mean_to_eccentric_base(M, e, method)
     else:
          E = np.zeros(len(M))
          for i in range(len(M)):
               E[i] = mean_to_eccentric_base(M[i], e, method)
          return E


# Convert mean anomaly to eccentric anomaly (Note: requires numerical methods)
def mean_to_eccentric_base(M: float, e: float, method="Newton-Raphson") -> float:
     if method == "Newton-Raphson":
          return NR(M, e)


# Directly convert mean anomaly to true anomaly
def mean_to_true(M, e, method="Newton-Raphson"):
     return eccentric_to_true(mean_to_eccentric(M, e, method), e)


# Newton-Raphson for solving E - e * sin(E) - M = 0
def NR(M: float, e: float, tol: float = 0.0001, max_iter: int = 10000) -> float:
     E_prev = M
     E_current = M - (M - e * np.sin(M) - M) / (1 - e * np.cos(M))
     seq_err = E_current - E_prev
     iter = 0
     while abs(seq_err) > tol:
          E_prev = E_current
          E_current = E_prev - (E_prev - e * np.sin(E_prev) - M) / (1 - e * np.cos(E_prev))
          seq_err = E_current - E_prev
          iter += 1
          if iter >=  max_iter:
               print("Error: failed to converge")
               break
     return E_current
