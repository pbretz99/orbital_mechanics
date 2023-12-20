from dataclasses import dataclass, field
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, 
    NavigationToolbar2Tk,
)
from matplotlib.axes import Axes
from typing import Optional

import numpy as np
import tkinter as tk

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


@dataclass
class OrbitViewer:
    window: tk.Tk
    orbit: EllipticOrbit = field(default_factory=EllipticOrbit)
    plot_params: PlotParams = field(default_factory=PlotParams)

    def plot(self):
        # Get figure and axes
        fig = Figure(
            figsize=(5, 5),
        )
        ax = fig.add_subplot(111)

        # Add everything to axis using OrbitPlotter
        plotter = OrbitPlotter(
            ax=ax, 
            orbit=self.orbit, 
            plot_params=self.plot_params
        )
        plotter.plot()

        canvas = FigureCanvasTkAgg(
            fig,
            self.window,
        ) 
        canvas.draw() 

        # placing the canvas on the Tkinter window 
        canvas.get_tk_widget().pack() 

        # creating the Matplotlib toolbar 
        toolbar = NavigationToolbar2Tk(
            canvas,
            self.window,
        ) 
        toolbar.update() 

        # placing the toolbar on the Tkinter window 
        canvas.get_tk_widget().pack() 

        


# the main Tkinter window 
window = tk.Tk() 

# setting the title 
window.title('Plotting in Tkinter') 

# dimensions of the main window 
window.geometry("500x500") 

viewer = OrbitViewer(
    window=window,
    orbit=EllipticOrbit(reference_true_anomaly_rad=np.pi / 2, eccentricity=0.5, omega_rad=np.pi / 3),
    plot_params=PlotParams(lookahead_min_alpha=0.2, lookahead_N_segs=6, trace_color=None)
)

# button that displays the plot 
plot_button = tk.Button(
    master=window, 
    command=viewer.plot, 
    height=2, 
    width=10, 
    text="Plot"
)

# place the button 
# in main window 
plot_button.pack() 

# run the gui 
window.mainloop() 
