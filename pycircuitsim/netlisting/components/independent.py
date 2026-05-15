from __future__ import annotations

from .base import Component


def _basic_source(prefix: str, id: str, nodes: tuple[str, str], dc_value: str,
                  ac_magnitude: str = "", ac_phase: str = "",
                  distof1_freq: str = "", distof1_magnitude: str = "1.0", distof1_phase: str = "0.0",
                  distof2_freq: str = "", distof2_magnitude: str = "1.0", distof2_phase: str = "0.0") -> str:
    parts = [
        f"{prefix}{id}",
        " ".join(nodes),
        f"DC {dc_value}",
        f"AC {ac_magnitude} {ac_phase if ac_phase else 0}" if ac_magnitude else None,
        f"DISTOF1 {distof1_freq} {distof1_magnitude} {distof1_phase}" if distof1_freq else None,
        f"DISTOF2 {distof2_freq} {distof2_magnitude} {distof2_phase}" if distof2_freq else None,
    ]
    return " ".join(filter(None, parts))


def _waveform_source(prefix: str, id: str, nodes: tuple[str, str], waveform: str, params: list) -> str:
    params_str = " ".join(str(p) for p in params)
    return f"{prefix}{id} {' '.join(nodes)} {waveform}({params_str})"


def V(
    self,
    id: str,
    nodes: tuple[str, str],
    dc_value: str,
    ac_magnitude: str = "",
    ac_phase: str = "",
    distof1_freq: str = "",
    distof1_magnitude: str = "1.0",
    distof1_phase: str = "0.0",
    distof2_freq: str = "",
    distof2_magnitude: str = "1.0",
    distof2_phase: str = "0.0",
) -> None:
    """Add an independent voltage source.

    id: Unique identifier.
    nodes: (positive_node, negative_node).
    dc_value: DC value.
    ac_magnitude: AC magnitude (optional).
    ac_phase: AC phase in degrees (optional).
    distof1_freq: Frequency for first distortion component (optional).
    distof1_magnitude: Magnitude for first distortion component (default ``"1.0"``).
    distof1_phase: Phase for first distortion component (default ``"0.0"``).
    distof2_freq: Frequency for second distortion component (optional).
    distof2_magnitude: Magnitude for second distortion component (default ``"1.0"``).
    distof2_phase: Phase for second distortion component (default ``"0.0"``).
    """
    s = _basic_source("V", id, nodes, dc_value, ac_magnitude, ac_phase,
                      distof1_freq, distof1_magnitude, distof1_phase,
                      distof2_freq, distof2_magnitude, distof2_phase)
    self._add_component(Component(id=id, spice_prefix="V", netlist_str=s))


def I(
    self,
    id: str,
    nodes: tuple[str, str],
    dc_value: str,
    ac_magnitude: str = "",
    ac_phase: str = "",
    distof1_freq: str = "",
    distof1_magnitude: str = "1.0",
    distof1_phase: str = "0.0",
    distof2_freq: str = "",
    distof2_magnitude: str = "1.0",
    distof2_phase: str = "0.0",
) -> None:
    """Add an independent current source.

    id: Unique identifier.
    nodes: (positive_node, negative_node).
    dc_value: DC value.
    ac_magnitude: AC magnitude (optional).
    ac_phase: AC phase in degrees (optional).
    distof1_freq: Frequency for first distortion component (optional).
    distof1_magnitude: Magnitude for first distortion component (default ``"1.0"``).
    distof1_phase: Phase for first distortion component (default ``"0.0"``).
    distof2_freq: Frequency for second distortion component (optional).
    distof2_magnitude: Magnitude for second distortion component (default ``"1.0"``).
    distof2_phase: Phase for second distortion component (default ``"0.0"``).
    """
    s = _basic_source("I", id, nodes, dc_value, ac_magnitude, ac_phase,
                      distof1_freq, distof1_magnitude, distof1_phase,
                      distof2_freq, distof2_magnitude, distof2_phase)
    self._add_component(Component(id=id, spice_prefix="I", netlist_str=s))


def VoltagePulse(
    self,
    id: str,
    nodes: tuple[str, str],
    initial_value: str,
    pulsed_value: str,
    delay_time: str = "0",
    rise_time: str = "0",
    fall_time: str = "0",
    pulse_width: str = "0",
    period: str = "0",
) -> None:
    """Add a voltage pulse source.

    id: Unique identifier.
    nodes: (positive_node, negative_node).
    initial_value: Value before the pulse.
    pulsed_value: Value during the pulse.
    delay_time: Delay before the pulse starts (default ``"0"``).
    rise_time: Rise time (default ``"0"``).
    fall_time: Fall time (default ``"0"``).
    pulse_width: Duration of the pulse (default ``"0"``).
    period: Period of the pulse cycle (default ``"0"``).
    """
    s = _waveform_source("V", id, nodes, "PULSE", [initial_value, pulsed_value, delay_time, rise_time, fall_time, pulse_width, period])
    self._add_component(Component(id=id, spice_prefix="V", netlist_str=s))


def CurrentPulse(
    self,
    id: str,
    nodes: tuple[str, str],
    initial_value: str,
    pulsed_value: str,
    delay_time: str = "0",
    rise_time: str = "0",
    fall_time: str = "0",
    pulse_width: str = "0",
    period: str = "0",
) -> None:
    """Add a current pulse source.

    id: Unique identifier.
    nodes: (positive_node, negative_node).
    initial_value: Value before the pulse.
    pulsed_value: Value during the pulse.
    delay_time: Delay before the pulse starts (default ``"0"``).
    rise_time: Rise time (default ``"0"``).
    fall_time: Fall time (default ``"0"``).
    pulse_width: Duration of the pulse (default ``"0"``).
    period: Period of the pulse cycle (default ``"0"``).
    """
    s = _waveform_source("I", id, nodes, "PULSE", [initial_value, pulsed_value, delay_time, rise_time, fall_time, pulse_width, period])
    self._add_component(Component(id=id, spice_prefix="I", netlist_str=s))


def VoltageSin(
    self,
    id: str,
    nodes: tuple[str, str],
    amplitude: str,
    frequency: str,
    offset: str = "0",
    delay: str = "0",
    damping_factor: str = "0",
    phase: str = "0",
) -> None:
    """Add a sinusoidal voltage source.

    id: Unique identifier.
    nodes: (positive_node, negative_node).
    amplitude: Peak amplitude.
    frequency: Frequency.
    offset: DC offset (default ``"0"``).
    delay: Delay before the waveform starts (default ``"0"``).
    damping_factor: Damping factor (default ``"0"``).
    phase: Phase shift in degrees (default ``"0"``).
    """
    s = _waveform_source("V", id, nodes, "SIN", [offset, amplitude, frequency, delay, damping_factor, phase])
    self._add_component(Component(id=id, spice_prefix="V", netlist_str=s))


def CurrentSin(
    self,
    id: str,
    nodes: tuple[str, str],
    amplitude: str,
    frequency: str,
    offset: str = "0",
    delay: str = "0",
    damping_factor: str = "0",
    phase: str = "0",
) -> None:
    """Add a sinusoidal current source.

    id: Unique identifier.
    nodes: (positive_node, negative_node).
    amplitude: Peak amplitude.
    frequency: Frequency.
    offset: DC offset (default ``"0"``).
    delay: Delay before the waveform starts (default ``"0"``).
    damping_factor: Damping factor (default ``"0"``).
    phase: Phase shift in degrees (default ``"0"``).
    """
    s = _waveform_source("I", id, nodes, "SIN", [offset, amplitude, frequency, delay, damping_factor, phase])
    self._add_component(Component(id=id, spice_prefix="I", netlist_str=s))


def VoltageExp(
    self,
    id: str,
    nodes: tuple[str, str],
    initial_value: str,
    pulsed_value: str,
    rise_delay_time: str = "0",
    rise_time_constant: str = "0",
    fall_delay_time: str = "0",
    fall_time_constant: str = "0",
) -> None:
    """Add an exponential voltage source.

    id: Unique identifier.
    nodes: (positive_node, negative_node).
    initial_value: Initial value before the pulse.
    pulsed_value: Value during the pulse.
    rise_delay_time: Delay before the exponential rise (default ``"0"``).
    rise_time_constant: Time constant for the exponential rise (default ``"0"``).
    fall_delay_time: Delay before the exponential fall (default ``"0"``).
    fall_time_constant: Time constant for the exponential fall (default ``"0"``).
    """
    s = _waveform_source("V", id, nodes, "EXP", [initial_value, pulsed_value, rise_delay_time, rise_time_constant, fall_delay_time, fall_time_constant])
    self._add_component(Component(id=id, spice_prefix="V", netlist_str=s))


def CurrentExp(
    self,
    id: str,
    nodes: tuple[str, str],
    initial_value: str,
    pulsed_value: str,
    rise_delay_time: str = "0",
    rise_time_constant: str = "0",
    fall_delay_time: str = "0",
    fall_time_constant: str = "0",
) -> None:
    """Add an exponential current source.

    id: Unique identifier.
    nodes: (positive_node, negative_node).
    initial_value: Initial value before the pulse.
    pulsed_value: Value during the pulse.
    rise_delay_time: Delay before the exponential rise (default ``"0"``).
    rise_time_constant: Time constant for the exponential rise (default ``"0"``).
    fall_delay_time: Delay before the exponential fall (default ``"0"``).
    fall_time_constant: Time constant for the exponential fall (default ``"0"``).
    """
    s = _waveform_source("I", id, nodes, "EXP", [initial_value, pulsed_value, rise_delay_time, rise_time_constant, fall_delay_time, fall_time_constant])
    self._add_component(Component(id=id, spice_prefix="I", netlist_str=s))


def VoltagePWL(
    self,
    id: str,
    nodes: tuple[str, str],
    time_value_pairs: list[tuple[str, str]],
    repeat_time: str = "",
    delay: str = "",
) -> None:
    """Add a piecewise-linear voltage source.

    id: Unique identifier.
    nodes: (positive_node, negative_node).
    time_value_pairs: List of (time, value) pairs defining the waveform.
    repeat_time: Repeat time for the waveform (optional).
    delay: Delay before the waveform starts (optional).
    """
    flat = [val for pair in time_value_pairs for val in pair]
    s = _waveform_source("V", id, nodes, "PWL", flat)
    if repeat_time:
        s += f" r={repeat_time}"
    if delay:
        s += f" td={delay}"
    self._add_component(Component(id=id, spice_prefix="V", netlist_str=s))


def CurrentPWL(
    self,
    id: str,
    nodes: tuple[str, str],
    time_value_pairs: list[tuple[str, str]],
    repeat_time: str = "",
    delay: str = "",
) -> None:
    """Add a piecewise-linear current source.

    id: Unique identifier.
    nodes: (positive_node, negative_node).
    time_value_pairs: List of (time, value) pairs defining the waveform.
    repeat_time: Repeat time for the waveform (optional).
    delay: Delay before the waveform starts (optional).
    """
    flat = [val for pair in time_value_pairs for val in pair]
    s = _waveform_source("I", id, nodes, "PWL", flat)
    if repeat_time:
        s += f" r={repeat_time}"
    if delay:
        s += f" td={delay}"
    self._add_component(Component(id=id, spice_prefix="I", netlist_str=s))


def VoltageTransientNoise(
    self,
    id: str,
    nodes: tuple[str, str],
    rms_noise_amplitude: str = "0",
    time_step: str = "0",
    alpha: str = "0",
    amplitude_1_f: str = "0",
    rts_amplitude: str = "0",
    trap_capture_time: str = "0",
    trap_emission_time: str = "0",
) -> None:
    """Add a transient noise voltage source.

    id: Unique identifier.
    nodes: (positive_node, negative_node).
    rms_noise_amplitude: RMS noise amplitude (default ``"0"``).
    time_step: Simulation time step (default ``"0"``).
    alpha: Exponent for 1/f noise (default ``"0"``).
    amplitude_1_f: Amplitude of 1/f noise (default ``"0"``).
    rts_amplitude: Random telegraph signal amplitude (default ``"0"``).
    trap_capture_time: Trap capture time for RTS noise (default ``"0"``).
    trap_emission_time: Trap emission time for RTS noise (default ``"0"``).
    """
    s = _waveform_source("V", id, nodes, "TRNOISE", [rms_noise_amplitude, time_step, alpha, amplitude_1_f, rts_amplitude, trap_capture_time, trap_emission_time])
    self._add_component(Component(id=id, spice_prefix="V", netlist_str=s))


def CurrentTransientNoise(
    self,
    id: str,
    nodes: tuple[str, str],
    rms_noise_amplitude: str = "0",
    time_step: str = "0",
    alpha: str = "0",
    amplitude_1_f: str = "0",
    rts_amplitude: str = "0",
    trap_capture_time: str = "0",
    trap_emission_time: str = "0",
) -> None:
    """Add a transient noise current source.

    id: Unique identifier.
    nodes: (positive_node, negative_node).
    rms_noise_amplitude: RMS noise amplitude (default ``"0"``).
    time_step: Simulation time step (default ``"0"``).
    alpha: Exponent for 1/f noise (default ``"0"``).
    amplitude_1_f: Amplitude of 1/f noise (default ``"0"``).
    rts_amplitude: Random telegraph signal amplitude (default ``"0"``).
    trap_capture_time: Trap capture time for RTS noise (default ``"0"``).
    trap_emission_time: Trap emission time for RTS noise (default ``"0"``).
    """
    s = _waveform_source("I", id, nodes, "TRNOISE", [rms_noise_amplitude, time_step, alpha, amplitude_1_f, rts_amplitude, trap_capture_time, trap_emission_time])
    self._add_component(Component(id=id, spice_prefix="I", netlist_str=s))
