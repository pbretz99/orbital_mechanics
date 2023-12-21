from dataclasses import dataclass, field
from matplotlib.axes import Axes
from typing import Optional

import numpy as np

from orbital_mechanics.orbits.elliptic import EllipticOrbit


@dataclass
class PlotParams:
    lookahead_color: Optional[str] = "C0"
    lookahead_s: float = 86400 # 1 day
    lookahead_N_segs: int = 12
    lookahead_min_alpha: float = 0.0
    trace_color: Optional[str] = "C0"
    trace_N_segs: int = 1000
    center_color: Optional[str] = "C0"


@dataclass
class OrbitPlotter:
    ax: Axes
    orbit: EllipticOrbit
    plot_params: PlotParams = field(default_factory=PlotParams)

    def add_center(self) -> None:
        if self.plot_params.center_color is not None:
            self.ax.scatter([0], [0], c=self.plot_params.center_color)
    
    def add_trace(self) -> None:
        if self.plot_params.trace_color is not None:
            trace = self.orbit.trace(N_segments=self.plot_params.trace_N_segs)
            self.ax.plot(trace.x, trace.y, c=self.plot_params.trace_color)

    def add_lookahead(self) -> None:
        if self.plot_params.lookahead_color is not None:
            t_s = np.linspace(0, self.plot_params.lookahead_s, self.plot_params.lookahead_N_segs + 1)
            trajectory = self.orbit.trajectory(t_s=t_s)
            t_norm = (t_s - t_s[0]) / (t_s[-1] - t_s[0])
            min_alpha = self.plot_params.lookahead_min_alpha
            alpha = (1 - t_norm) * (1 - min_alpha) + min_alpha
            self.ax.scatter(trajectory.x, trajectory.y, c="C0", alpha=alpha)

    def plot(self) -> None:
        self.add_trace()
        self.add_lookahead()
        self.add_center()
        self.ax.axis("equal")
        self.ax.set_xticks([])
        self.ax.set_yticks([])
