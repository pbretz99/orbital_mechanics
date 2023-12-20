from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np

from orbital_mechanics.utilities import is_ND_vec


@dataclass
class Trajectory:
    t: np.ndarray
    x: np.ndarray
    y: np.ndarray

    def __post_init__(self):
        self.N = self.t.shape[0]
        assert is_ND_vec(self.t, self.N)
        assert is_ND_vec(self.x, self.N)
        assert is_ND_vec(self.y, self.N)


class OrbitBase:
    @abstractmethod
    def trajectory(self, t_s: np.ndarray) -> Trajectory:
        pass
