from tkinter import *

import numpy as np

from orbital_mechanics.visualization.tk_app.parameters import (
    FloatParameter,
    Bound,
)
from orbital_mechanics.visualization.tk_app.parameters_frame import (
    ParametersFrame
)
from orbital_mechanics.visualization.tk_app.viewer import OrbitViewer

def build_app() -> Tk:
    # the main Tkinter window 
    window = Tk() 

    # setting the title 
    window.title('Elliptic Orbit') 

    # dimensions of the main window 
    window.geometry("800x500") 

    plot_frm = Frame(window)
    plot_frm.grid(row=0, column=1)
    viewer_frm = Frame(plot_frm)
    viewer = OrbitViewer(
        window=viewer_frm,
    )
    viewer_frm.grid(row=1, column=0)

    true_anomaly_param = FloatParameter(
        "nu",
        "nu must be in [0, 360)",
        orbit_key="reference_true_anomaly_rad",
        default_input="0.0",
        units="deg",
        lower=Bound(0),
        upper=Bound(360, strict=True),
        input_to_internal_val_factor=np.pi / 180
    )
    eccentricity_param = FloatParameter(
        "e", 
        "e must be in [0, 1)", 
        orbit_key="eccentricity", 
        default_input="0.0",
        lower=Bound(0), 
        upper=Bound(0.99)
    )
    omega_param = FloatParameter(
        "Omega", 
        "Omega must be in [0, 360)", 
        orbit_key="omega_rad", 
        default_input="0.0",
        units="deg", 
        lower=Bound(0), 
        upper=Bound(360, strict=True), 
        input_to_internal_val_factor=np.pi / 180
    )

    input_frm = Frame(window)
    input_collection = ParametersFrame(
        frame=input_frm, 
        parameters_list=[
            true_anomaly_param, 
            eccentricity_param, 
            omega_param
        ],
    )

    # button that displays the plot 
    plot_button = Button(
        master=plot_frm, 
        command=lambda : input_collection.render(viewer=viewer), 
        text="Plot"
    )

    # place the button 
    # in main window 
    plot_button.grid(column=0, row=0)
    viewer.plot()

    return window
