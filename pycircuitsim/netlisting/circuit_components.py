import inspect
from typing import Any, Callable, Generic, ParamSpec

from .components.passive import Capacitor, CurrentControlledSwitch, Inductor, LosslessTransmissionLine, MutualInductance, Resistor, VoltageControlledSwitch
from .components.semiconductors import BJT, Diode, JFET, Mosfet
from .components.independent import (
    CurrentExp,
    CurrentPulse,
    CurrentPWL,
    CurrentSin,
    CurrentSource,
    CurrentTransientNoise,
    VoltageExp,
    VoltagePulse,
    VoltagePWL,
    VoltageSin,
    VoltageSource,
    VoltageTransientNoise,
)
from .components.dependent import (
    BehavioralSource,
    CurrentControlledCurrentSource,
    CurrentControlledVoltageSource,
    VoltageControlledCurrentSource,
    VoltageControlledVoltageSource,
)
from .components.instance import SubCircuitInstance, OsdiInstance

P = ParamSpec("P")


class ComponentMethod(Generic[P]):
    def __init__(self, component_cls: Callable[P, Any]) -> None:
        self.component_cls = component_cls

    def __get__(self, obj, objtype=None) -> Callable[P, None]:
        if obj is None:
            return self  # type: ignore[return-value]
        cls = self.component_cls
        def method(*args, **kwargs):
            obj._add_component(cls(*args, **kwargs))
        method.__doc__ = cls.__init__.__doc__
        method.__signature__ = inspect.signature(cls)
        return method


class CircuitComponents:
    R                     = ComponentMethod(Resistor)
    L                     = ComponentMethod(Inductor)
    C                     = ComponentMethod(Capacitor)
    K                     = ComponentMethod(MutualInductance)
    S                     = ComponentMethod(VoltageControlledSwitch)
    W                     = ComponentMethod(CurrentControlledSwitch)
    T                     = ComponentMethod(LosslessTransmissionLine)
    D                     = ComponentMethod(Diode)
    J                     = ComponentMethod(JFET)
    M                     = ComponentMethod(Mosfet)
    Q                     = ComponentMethod(BJT)
    V                     = ComponentMethod(VoltageSource)
    I                     = ComponentMethod(CurrentSource)
    G                     = ComponentMethod(VoltageControlledCurrentSource)
    E                     = ComponentMethod(VoltageControlledVoltageSource)
    F                     = ComponentMethod(CurrentControlledCurrentSource)
    H                     = ComponentMethod(CurrentControlledVoltageSource)
    B                     = ComponentMethod(BehavioralSource)
    X                     = ComponentMethod(SubCircuitInstance)
    N                     = ComponentMethod(OsdiInstance)
    VoltagePulse          = ComponentMethod(VoltagePulse)
    CurrentPulse          = ComponentMethod(CurrentPulse)
    VoltageSin            = ComponentMethod(VoltageSin)
    CurrentSin            = ComponentMethod(CurrentSin)
    VoltageExp            = ComponentMethod(VoltageExp)
    CurrentExp            = ComponentMethod(CurrentExp)
    VoltagePWL            = ComponentMethod(VoltagePWL)
    CurrentPWL            = ComponentMethod(CurrentPWL)
    VoltageTransientNoise = ComponentMethod(VoltageTransientNoise)
    CurrentTransientNoise = ComponentMethod(CurrentTransientNoise)
