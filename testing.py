from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, 
    NavigationToolbar2Tk,
)
from tkinter import *
from typing import Optional, Any

import numpy as np

from orbital_mechanics.orbits.elliptic import EllipticOrbit
from orbital_mechanics.visualization.plotter import (
    PlotParams,
    OrbitPlotter,
)


@dataclass
class ParameterBase(ABC):
    label: str
    error_msg: str
    units: Optional[str] = None

    @abstractmethod
    def validate_input(self, input: str) -> Any:
        pass


@dataclass
class Bound:
    value: float
    strict: bool = False

@dataclass
class FloatParameter(ParameterBase):
    lower: Optional[Bound] = None
    upper: Optional[Bound] = None

    def validate_input(self, input: str) -> float:
        input_float = float(input)
        if self.lower is not None:
            if input_float < self.lower.value:
                raise ValueError
            if self.lower.strict and input_float == self.lower.value:
                raise ValueError
        if self.upper is not None:
            if input_float > self.upper.value:
                raise ValueError
            if self.upper.strict and input_float == self.upper.value:
                raise ValueError
        return input_float
        

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

        


# the main Tkinter window 
window = Tk() 

# setting the title 
window.title('Plotting in Tkinter') 

# dimensions of the main window 
window.geometry("700x500") 

viewer_frm = Frame(window)
viewer = OrbitViewer(
    window=viewer_frm,
)
viewer_frm.grid(row=0, column=2)

input_frm = Frame(window)
eccentricity_param = FloatParameter("e", "e must be in [0, 1)", lower=Bound(0), upper=Bound(1, strict=True))

e_frm = Frame(input_frm)
e_lbl = Label(e_frm, text=f"{eccentricity_param.label} : ")
e_txt = Entry(e_frm, width=6)
e_err_lbl = Label(e_frm, text="", width=15)
for i, widget in enumerate([e_lbl, e_txt, e_err_lbl]):
    widget.grid(row=0, column=i)
e_frm.grid(row=0, column=0)
input_frm.grid(row=0, column=0)

def render():
    try:
        e = eccentricity_param.validate_input(e_txt.get())
        e_err_lbl.configure(text="")
        viewer.orbit.eccentricity = e
    except:
        e_err_lbl.configure(text=eccentricity_param.error_msg, fg="red")
    viewer.plot()

# button that displays the plot 
plot_button = Button(
    master=window, 
    command=render, 
    text="Plot"
)

# place the button 
# in main window 
plot_button.grid(column=1, row=0)
viewer.plot()

# run the gui 
window.mainloop() 
