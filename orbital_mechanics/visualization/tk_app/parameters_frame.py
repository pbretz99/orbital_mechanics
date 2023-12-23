from dataclasses import dataclass
from tkinter import *

from orbital_mechanics.visualization.tk_app.parameters import (
    ParameterBase,
    ParameterCollection,
)
from orbital_mechanics.visualization.tk_app.viewer import (
    OrbitViewer
)


@dataclass
class ParametersFrame:
    frame: Frame
    parameters_list: list[ParameterBase]

    def __post_init__(self):
        self.collection_list = self._create_collection_list()
        self.frame.grid(row=0, column=0, sticky="N")

    def _create_collection_list(self) -> list[ParameterCollection]:
        collection_list = []
        for i, param in enumerate(self.parameters_list):
            param_collection = param.build_collection(master=self.frame)
            param_collection.set_grid(row=i)
            collection_list.append(param_collection)
        return collection_list

    def render(self, viewer: OrbitViewer) -> None:
        error_flag = False
        vals_dict = {}
        for param, param_collection in zip(self.parameters_list, self.collection_list):
            try:
                val = param.validate_input(param_collection.entry_txt.get())
                param_collection.error_lbl.configure(text="")
                vals_dict[param.orbit_key] = val
            except:
                param_collection.error_lbl.configure(text=param.error_msg, fg="red")
                error_flag = True
        if not error_flag:
            for orbit_key in vals_dict.keys():
                setattr(viewer.orbit, orbit_key, vals_dict[orbit_key])
            viewer.plot()
