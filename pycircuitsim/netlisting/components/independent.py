from .base import Component


# Class: Basic Source <<<
class BasicSource(Component):
    def __init__(
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
    ):
        """
        Spice basic source component with DC, AC, and distortion parameters.

        Args:
            id: Unique identifier for the source.
            nodes: (positive_node, negative_node).
            dc_value: DC value for the source.
            ac_magnitude: AC magnitude (optional).
            ac_phase: AC phase in degrees (optional).
            distof1_freq: Frequency for the first distortion component (optional).
            distof1_magnitude: Magnitude for the first distortion component (default 1.0).
            distof1_phase: Phase for the first distortion component in degrees (default 0.0).
            distof2_freq: Frequency for the second distortion component (optional).
            distof2_magnitude: Magnitude for the second distortion component (default 1.0).
            distof2_phase: Phase for the second distortion component in degrees (default 0.0).
        """
        self.id = id
        self.nodes = nodes
        self.dc_value = dc_value
        self.ac_magnitude = ac_magnitude
        self.ac_phase = ac_phase
        self.distof1_freq = distof1_freq
        self.distof1_magnitude = distof1_magnitude
        self.distof1_phase = distof1_phase
        self.distof2_freq = distof2_freq
        self.distof2_magnitude = distof2_magnitude
        self.distof2_phase = distof2_phase

    def __str__(self):
        parts = [
            f"{self.spice_prefix}{self.id}",
            " ".join(self.nodes),
            f"DC {self.dc_value}",
            f"AC {self.ac_magnitude} {self.ac_phase if self.ac_phase else 0}" if self.ac_magnitude else None,
            f"DISTOF1 {self.distof1_freq} {self.distof1_magnitude} {self.distof1_phase}" if self.distof1_freq else None,
            f"DISTOF2 {self.distof2_freq} {self.distof2_magnitude} {self.distof2_phase}" if self.distof2_freq else None,
        ]
        return " ".join(filter(None, parts))


class VoltageSource(BasicSource):
    """Spice independent voltage source."""
    @property
    def spice_prefix(self):
        return "V"


class CurrentSource(BasicSource):
    """Spice independent current source."""
    @property
    def spice_prefix(self):
        return "I"
# >>>


# Class: Waveform Source <<<
class WaveformSource(Component):
    def __init__(self, id: str, nodes: tuple[str, ...], waveform: str, params: list):
        self.id = id
        self.nodes = nodes
        self.waveform = waveform
        self.params = params

    def __str__(self):
        params_str = " ".join(str(p) for p in self.params)
        return f"{self.spice_prefix}{self.id} {' '.join(self.nodes)} {self.waveform}({params_str})"


class PulseSource(WaveformSource):
    def __init__(
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
    ):
        """
        Spice pulse source component.

        Args:
            id: Unique identifier for the pulse source.
            nodes: (positive_node, negative_node).
            initial_value: Initial value before the pulse.
            pulsed_value: Value during the pulse.
            delay_time: Time delay before the pulse starts (default "0").
            rise_time: Rise time from initial to pulsed value (default "0").
            fall_time: Fall time back to initial value (default "0").
            pulse_width: Duration of the pulse (default "0").
            period: Period of the pulse cycle (default "0").
        """
        super().__init__(id, nodes, "PULSE", [initial_value, pulsed_value, delay_time, rise_time, fall_time, pulse_width, period])


class VoltagePulse(PulseSource):
    """Spice voltage pulse source."""
    @property
    def spice_prefix(self):
        return "V"


class CurrentPulse(PulseSource):
    """Spice current pulse source."""
    @property
    def spice_prefix(self):
        return "I"


class SinusoidalSource(WaveformSource):
    def __init__(
        self,
        id: str,
        nodes: tuple[str, str],
        amplitude: str,
        frequency: str,
        offset: str = "0",
        delay: str = "0",
        damping_factor: str = "0",
        phase: str = "0",
    ):
        """
        Spice sinusoidal source component.

        Args:
            id: Unique identifier for the sinusoidal source.
            nodes: (positive_node, negative_node).
            amplitude: Peak amplitude of the waveform.
            frequency: Frequency of the waveform.
            offset: DC offset (default "0").
            delay: Time delay before the waveform starts (default "0").
            damping_factor: Damping factor (default "0").
            phase: Phase shift in degrees (default "0").
        """
        super().__init__(id, nodes, "SIN", [offset, amplitude, frequency, delay, damping_factor, phase])


class VoltageSin(SinusoidalSource):
    """Spice sinusoidal voltage source."""
    @property
    def spice_prefix(self):
        return "V"


class CurrentSin(SinusoidalSource):
    """Spice sinusoidal current source."""
    @property
    def spice_prefix(self):
        return "I"


class ExponentialSource(WaveformSource):
    def __init__(
        self,
        id: str,
        nodes: tuple[str, str],
        initial_value: str,
        pulsed_value: str,
        rise_delay_time: str = "0",
        rise_time_constant: str = "0",
        fall_delay_time: str = "0",
        fall_time_constant: str = "0",
    ):
        """
        Spice exponential source component.

        Args:
            id: Unique identifier for the exponential source.
            nodes: (positive_node, negative_node).
            initial_value: Initial value before the pulse.
            pulsed_value: Value during the pulse.
            rise_delay_time: Delay before the exponential rise begins (default "0").
            rise_time_constant: Time constant for the exponential rise (default "0").
            fall_delay_time: Delay before the exponential fall begins (default "0").
            fall_time_constant: Time constant for the exponential fall (default "0").
        """
        super().__init__(id, nodes, "EXP", [initial_value, pulsed_value, rise_delay_time, rise_time_constant, fall_delay_time, fall_time_constant])


class VoltageExp(ExponentialSource):
    """Spice exponential voltage source."""
    @property
    def spice_prefix(self):
        return "V"


class CurrentExp(ExponentialSource):
    """Spice exponential current source."""
    @property
    def spice_prefix(self):
        return "I"


class PieceWiseLinearSource(WaveformSource):
    def __init__(
        self,
        id: str,
        nodes: tuple[str, str],
        time_value_pairs: list[tuple[str, str]],
        repeat_time: str = "",
        delay: str = "",
    ):
        """
        Spice piecewise linear (PWL) source component.

        Args:
            id: Unique identifier for the PWL source.
            nodes: (positive_node, negative_node).
            time_value_pairs: List of (time, value) pairs defining the waveform.
            repeat_time: Repeat time for the waveform (optional).
            delay: Delay before the waveform starts (optional).
        """
        super().__init__(id, nodes, "PWL", [val for pair in time_value_pairs for val in pair])
        self.repeat_time = repeat_time
        self.delay = delay

    def __str__(self):
        parts = [super().__str__()]
        if self.repeat_time:
            parts.append(f"r={self.repeat_time}")
        if self.delay:
            parts.append(f"td={self.delay}")
        return " ".join(parts)


class VoltagePWL(PieceWiseLinearSource):
    """Spice piecewise linear voltage source."""
    @property
    def spice_prefix(self):
        return "V"


class CurrentPWL(PieceWiseLinearSource):
    """Spice piecewise linear current source."""
    @property
    def spice_prefix(self):
        return "I"


class TransientNoiseSource(WaveformSource):
    def __init__(
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
    ):
        """
        Spice transient noise source component.

        Args:
            id: Unique identifier for the transient noise source.
            nodes: (positive_node, negative_node).
            rms_noise_amplitude: RMS noise amplitude (default "0").
            time_step: Simulation time step (default "0").
            alpha: Exponent for 1/f noise (default "0").
            amplitude_1_f: Amplitude of 1/f noise (default "0").
            rts_amplitude: Random telegraph signal amplitude (default "0").
            trap_capture_time: Trap capture time for RTS noise (default "0").
            trap_emission_time: Trap emission time for RTS noise (default "0").
        """
        super().__init__(id, nodes, "TRNOISE", [rms_noise_amplitude, time_step, alpha, amplitude_1_f, rts_amplitude, trap_capture_time, trap_emission_time])


class VoltageTransientNoise(TransientNoiseSource):
    """Spice transient noise voltage source."""
    @property
    def spice_prefix(self):
        return "V"


class CurrentTransientNoise(TransientNoiseSource):
    """Spice transient noise current source."""
    @property
    def spice_prefix(self):
        return "I"
# >>>
