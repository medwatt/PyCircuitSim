from .waveforms import (
    WaveformSegment,
    DelaySegment,
    PulseSegment,
    SquareSegment,
    TriangleSegment,
    SawtoothSegment,
)


class WaveformGenerator:
    """Generates the full waveform from added waveform segments."""

    def __init__(
        self, scale: str = "n", transition_time: float = 0.0, dc_baseline: float = 0.0
    ):
        self.scale = scale
        if transition_time <= 0.0:
            raise ValueError("Transition time must be greater than zero.")
        self.transition_time = transition_time
        self.dc_baseline = dc_baseline
        self.segments: list[WaveformSegment] = []

    def delay(self, duration: float):
        """Add a delay segment."""
        self.segments.append(DelaySegment(duration))

    def pulse(
        self,
        duration: float,
        pulse_value: float,
        delay_before: float = 0.0,
        delay_after: float = 0.0,
        cycles: int = 1,
    ):
        """Add a pulse segment."""
        self.segments.append(
            PulseSegment(
                duration,
                pulse_value,
                delay_before,
                delay_after,
                self.transition_time,
                cycles,
            )
        )

    def square(
        self,
        duration: float,
        start_value: float,
        end_value: float,
        delay_before: float = 0.0,
        delay_after: float = 0.0,
        cycles: int = 1,
    ):
        self.segments.append(
            SquareSegment(
                duration,
                start_value,
                end_value,
                delay_before,
                delay_after,
                self.transition_time,
                cycles,
            )
        )

    def triangle(
        self,
        duration: float,
        peak_value: float,
        delay_before: float = 0.0,
        delay_after: float = 0.0,
        cycles: int = 1,
    ):
        """Add a triangle wave segment."""
        self.segments.append(
            TriangleSegment(
                duration,
                peak_value,
                delay_before,
                delay_after,
                self.transition_time,
                cycles,
            )
        )

    def sawtooth(
        self,
        duration: float,
        start_value: float,
        end_value: float,
        delay_before: float = 0.0,
        delay_after: float = 0.0,
        cycles: int = 1,
    ):
        """Add a sawtooth wave segment."""
        self.segments.append(
            SawtoothSegment(
                duration,
                start_value,
                end_value,
                delay_before,
                delay_after,
                self.transition_time,
                cycles,
            )
        )

    def generate(self) -> list[tuple[str, str]]:
        """Generate the full waveform as a list of (time, value) tuples."""
        times = [0.0]
        values = [0.0]
        last_time = times[-1]
        last_value = values[-1]

        for segment in self.segments:
            segment_times, segment_values = segment.generate(last_time, last_value)
            times.extend(segment_times)
            values.extend(segment_values)
            last_time = times[-1]
            last_value = values[-1]

        # Format times according to scale
        formatted_times = [f"{str(t)}{self.scale}" for t in times]
        values_str = [f"{str(v + self.dc_baseline)}" for v in values]
        waveform = list(zip(formatted_times, values_str))
        return waveform
