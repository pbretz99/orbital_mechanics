from dataclasses import dataclass

import numpy as np

from orbital_mechanics.constants import M_EARTH, G, PI
from orbital_mechanics.orbits.anomalies import mean_to_true, true_to_mean
from orbital_mechanics.orbits.orbit_base import OrbitBase, Trajectory


@dataclass
class EllipticOrbit(OrbitBase):
    reference_true_anomaly_rad: float = 0.0
    eccentricity: float = 0.0
    semimajor_axis_m: float = 1e8
    omega_rad: float = 0.0
    mass_kg: float = 1e3
    center_mass_kg: float = M_EARTH

    # mu: gravitational parameter, a function of a and m, units of [m^3 * s^-2]
    @property
    def mu_m_cubed_per_s_sq(self) -> float:
        return G * (self.mass_kg + self.center_mass_kg)
    
    # T: orbital period, a function of a and mu, units of [s]
    @property
    def orbital_period_s(self) -> float:
        return 2 * PI * np.sqrt(self.semimajor_axis_m ** 3 / self.mu_m_cubed_per_s_sq)

    # p: semi-latus rectum, a function of a and e
    @property
    def semilatus_rectum_m(self) -> float:
        return self.semimajor_axis_m * (1 - self.eccentricity ** 2)
    
    # periapsis, the shortest distance from the orbit to its center
    @property
    def periapsis_m(self):
        return self.semilatus_rectum_m / (1 + self.eccentricity)
    
    # apoapsis, the longest distance from the orbit to its center
    @property
    def apoapsis_m(self):
        return self.semilatus_rectum_m / (1 - self.eccentricity)
    
    # Return the orbital radius r for a given true anomaly nu, units of [m]
    def radius_m(self, true_anomaly_rad: np.ndarray) -> np.ndarray:
        return self.semilatus_rectum_m / (1 + self.eccentricity * np.cos(true_anomaly_rad))
    
    # Return orbital speed for a given true anomaly nu, units of [m/s]
    def orbital_speed_m_per_s(self, true_anomaly_rad: np.ndarray) -> np.ndarray:
        return np.sqrt(self.mu_m_cubed_per_s_sq * (2 / self.radius_m(true_anomaly_rad) - 1 / self.semimajor_axis_m))
    
    # Return orbital tangent vector for a given true anomaly nu
    def unit_tangent(self, true_anomaly_rad: np.ndarray) -> np.ndarray:
        e = self.eccentricity
        r = self.radius_m(true_anomaly_rad)
        dr_dnu = (self.semilatus_rectum_m * e * np.sin(true_anomaly_rad)) / (1 + e * np.cos(true_anomaly_rad)) ** 2
        theta = true_anomaly_rad + self.omega_rad
        tangent = np.array([dr_dnu * np.cos(theta) - r * np.sin(theta), dr_dnu * np.sin(theta) + r * np.cos(theta)])
        if np.linalg.norm(tangent) > 0:
            return tangent / np.linalg.norm(tangent)
        else:
            return tangent
    
    def unit_normal(self, true_anomaly_rad: np.ndarray) -> np.ndarray:
        x, y = self.unit_tangent(true_anomaly_rad)
        return np.array([-y, x])

    # Return orbital tangent vector for a given true anomaly nu, units of [m/s]
    def velocity_vector(self, true_anomaly_rad: np.ndarray) -> np.ndarray:
        return self.orbital_speed_m_per_s(true_anomaly_rad) * self.unit_tangent(true_anomaly_rad)
    
    # Return x, y pair (as a np array) for true anomaly nu
    def position_vector(self, true_anomaly_rad: np.ndarray) -> np.ndarray:
        r = self.radius_m(true_anomaly_rad)
        theta = true_anomaly_rad + self.omega_rad
        return np.array([r * np.cos(theta), r * np.sin(theta)])

    # Rotation matrix that takes a vector defined by the T-V frame to i-j
    def TN_to_ij_mat(self, nu):
        T = self.unit_tangent(nu)
        N = self.unit_normal(nu)
        return np.stack((T, N), axis=1)

    # x, y coordinates for true anomaly nu value(s)
    def points(self, nu: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        r = self.radius_m(nu)
        x, y = r * np.cos(nu + self.omega_rad), r * np.sin(nu + self.omega_rad)
        return x, y
    
    # Find true anomaly t units in the future after current true anomaly nu
    def trajectory(self, t_s: np.ndarray) -> Trajectory:
        reference_M = true_to_mean(self.reference_true_anomaly_rad, self.eccentricity)
        M = reference_M + (t_s / self.orbital_period_s) * 2 * PI
        nu = mean_to_true(M, self.eccentricity)
        x, y = self.points(nu)
        return Trajectory(t_s, x, y)

    def trace(self, N_segments: int = 1000) -> Trajectory:
        T = self.orbital_period_s
        t_s = np.linspace(0, T, N_segments + 1)
        return self.trajectory(t_s=t_s)
