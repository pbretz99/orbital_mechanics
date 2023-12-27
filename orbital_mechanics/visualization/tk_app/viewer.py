from dataclasses import dataclass, field
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, 
)
from tkinter import *

from orbital_mechanics.orbits.elliptic import EllipticOrbit
from orbital_mechanics.visualization.plotter import (
    PlotParams,
    OrbitPlotter,
)


@dataclass
class OrbitViewer:
    window: Tk
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
        canvas.get_tk_widget().grid(column=0, row=0)
