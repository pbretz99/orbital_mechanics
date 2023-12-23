from abc import ABC, abstractmethod
from dataclasses import dataclass
from tkinter import *
from typing import Optional, Any


@dataclass
class ParameterCollection:
    name_lbl: Label
    entry_txt: Entry
    units_lbl: Label
    error_lbl: Label

    def set_grid(self, row: int) -> None:
        self.name_lbl.grid(row=row, column=0, sticky="E")
        self.entry_txt.grid(row=row, column=1)
        self.units_lbl.grid(row=row, column=2, sticky="W")
        self.error_lbl.grid(row=row, column=3, sticky="W")


@dataclass
class ParameterBase(ABC):
    label: str
    error_msg: str
    orbit_key: str
    default_input: str
    units: Optional[str] = None

    entry_width = 5
    units_width = 5
    error_msg_width = 25
    @abstractmethod
    def validate_input(self, input: str) -> Any:
        pass

    @property
    def units_string(self) -> str:
        if self.units is not None:
            return self.units
        return ""

    def build_collection(self, master: Frame) -> ParameterCollection:
        param_collection = ParameterCollection(
            name_lbl=Label(master=master, text=f"{self.label} = "),
            entry_txt=Entry(master=master, width=self.entry_width),
            units_lbl=Label(master=master, text=self.units_string, width=self.units_width),
            error_lbl=Label(master=master, text="", width=self.error_msg_width)
        )
        param_collection.entry_txt.insert(END, self.default_input)
        return param_collection


@dataclass
class Bound:
    value: float
    strict: bool = False


@dataclass
class FloatParameter(ParameterBase):
    lower: Optional[Bound] = None
    upper: Optional[Bound] = None
    input_to_internal_val_factor: float = 1.0

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
        return input_float * self.input_to_internal_val_factor
