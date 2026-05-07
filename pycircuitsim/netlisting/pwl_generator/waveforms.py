from abc import ABC, abstractmethod

# abstract class <<<
class WaveformSegment(ABC):
    """Abstract base class for waveform segments."""
    def __init__(self):
        self.times = []
        self.values = []

    @abstractmethod
    def generate(self, last_time: float, last_value: float) -> tuple[list[float], list[float]]:
        """Generate time and value points for this segment."""
        pass

    def add_delay(self, delay, last_time, last_value):
        if delay > 0:
            last_time += delay
            self.times.append(last_time)
            self.values.append(last_value)
        return last_time

    def add_transition(self, last_time, last_value, transition_time, transition_value):
        last_time += transition_time
        last_value += transition_value
        self.times.append(last_time)
        self.values.append(last_value)
        return last_time, last_value

# >>>

# delay segment <<<
class DelaySegment(WaveformSegment):
    """Represents a delay segment in the waveform."""

    def __init__(self, duration: float):
        self.duration = duration

    def generate(self, last_time: float, last_value: float) -> tuple[list[float], list[float]]:
        times = [last_time + self.duration]
        values = [last_value]
        return times, values
# >>>

# pulse segment <<<
class PulseSegment(WaveformSegment):
    """Represents a pulse segment in the waveform."""

    def __init__(
        self,
        duration: float,
        pulse_value: float,
        delay_before: float = 0.0,
        delay_after: float = 0.0,
        transition_time: float = 0.0,
        cycles: int = 1,
    ):
        self.duration = duration
        self.pulse_value = pulse_value
        self.delay_before = delay_before
        self.delay_after = delay_after
        self.transition_time = transition_time
        self.cycles = cycles
        super().__init__()

    def generate(self, last_time: float, last_value: float) -> tuple[list[float], list[float]]:

        for _ in range(self.cycles):
            # Delay before pulse
            last_time = self.add_delay(self.delay_before, last_time, last_value)

            # Transition to pulse value
            last_time, last_value = self.add_transition(last_time, last_value, self.transition_time, self.pulse_value)

            # Pulse duration
            last_time += self.duration
            self.times.append(last_time)
            self.values.append(last_value)

            # Transition back to base value
            last_time, last_value = self.add_transition(last_time, last_value, self.transition_time, -self.pulse_value)

            # Delay after pulse
            last_time = self.add_delay(self.delay_after, last_time, last_value)

        return self.times, self.values
# >>>

# square segment <<<
class SquareSegment(WaveformSegment):
    """Represents a square wave segment in the waveform."""

    def __init__(
        self,
        duration: float,
        start_value: float,
        end_value: float,
        delay_before: float = 0.0,
        delay_after: float = 0.0,
        transition_time: float = 0.0,
        cycles: int = 1,
    ):
        self.duration = duration
        self.start_value = start_value
        self.end_value = end_value
        self.delay_before = delay_before
        self.delay_after = delay_after
        self.transition_time = transition_time
        self.cycles = cycles
        super().__init__()

    def generate(self, last_time: float, last_value: float) -> tuple[list[float], list[float]]:
        half_duration = self.duration / 2

        for _ in range(self.cycles):
            # Delay before
            last_time = self.add_delay(self.delay_before, last_time, last_value)

            # Transition to start value
            last_time, last_value = self.add_transition(last_time, last_value, self.transition_time, self.start_value)

            # Hold start value
            last_time += half_duration
            self.times.append(last_time)
            self.values.append(last_value)

            # Transition to end value
            last_time, last_value = self.add_transition(last_time, last_value, self.transition_time, self.end_value - self.start_value)

            # Hold end value
            last_time += half_duration
            self.times.append(last_time)
            self.values.append(last_value)

            # Transition back to base value
            last_time, last_value = self.add_transition(last_time, last_value, self.transition_time, -self.end_value)

            # Delay after
            last_time = self.add_delay(self.delay_after, last_time, last_value)

        return self.times, self.values
# >>>

# triangle segment <<<
class TriangleSegment(WaveformSegment):
    """Represents a triangle wave segment in the waveform."""

    def __init__(
        self,
        duration: float,
        peak_value: float,
        delay_before: float = 0.0,
        delay_after: float = 0.0,
        transition_time: float = 0.0,
        cycles: int = 1,
    ):
        self.duration = duration
        self.peak_value = peak_value
        self.delay_before = delay_before
        self.delay_after = delay_after
        self.transition_time = transition_time
        self.cycles = cycles
        super().__init__()

    def generate(self, last_time: float, last_value: float) -> tuple[list[float], list[float]]:
        half_duration = self.duration / 2

        for _ in range(self.cycles):
            # Delay before
            last_time = self.add_delay(self.delay_before, last_time, last_value)

            # Rise to peak
            last_time, last_value = self.add_transition(last_time, last_value, half_duration, self.peak_value)

            # Fall back to base
            last_time, last_value = self.add_transition(last_time, last_value, half_duration, -self.peak_value)

            # Delay after
            last_time = self.add_delay(self.delay_after, last_time, last_value)

        return self.times, self.values
# >>>

# sawtooth segment <<<
class SawtoothSegment(WaveformSegment):
    """Represents a sawtooth wave segment in the waveform."""

    def __init__(
        self,
        duration: float,
        start_value: float,
        end_value: float,
        delay_before: float = 0.0,
        delay_after: float = 0.0,
        transition_time: float = 0.0,
        cycles: int = 1,
    ):
        self.duration = duration
        self.start_value = start_value
        self.end_value = end_value
        self.delay_before = delay_before
        self.delay_after = delay_after
        self.transition_time = transition_time
        self.cycles = cycles
        super().__init__()

    def generate(self, last_time: float, last_value: float) -> tuple[list[float], list[float]]:
        for _ in range(self.cycles):
            # Delay before
            last_time = self.add_delay(self.delay_before, last_time, last_value)

            # Transition to pulse value
            last_time, last_value = self.add_transition(last_time, last_value, self.transition_time, self.start_value)

            # Ramp to end value
            last_time, last_value = self.add_transition(last_time, last_value, self.duration, self.end_value - self.start_value)

            # Transition back to base value
            last_time, last_value = self.add_transition(last_time, last_value, self.transition_time, -self.end_value)

            # Delay after
            last_time = self.add_delay(self.delay_after, last_time, last_value)

        return self.times, self.values
# >>>
