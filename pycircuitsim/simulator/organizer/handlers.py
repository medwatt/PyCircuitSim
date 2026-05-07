import re
from abc import ABC, abstractmethod


# abstract base <<<
class Handler(ABC):
    """Abstract base class for handlers in the chain."""
    def __init__(self, key, successor=None):
        self.key = key
        self.successor = successor

    @abstractmethod
    def handle(self, vector_name, data, data_organizer):
        pass


class DefaultHandler(Handler):
    """Catch-all handler; stores vectors nested under key by dotted name."""

    def handle(self, vector_name, data, data_organizer):
        hierarchy = vector_name.split(".")
        d = data_organizer.data.setdefault(self.key, {})
        for level in hierarchy[:-1]:
            d = d.setdefault(level, {})
        d[hierarchy[-1]] = data
# >>>


# name handlers <<<
class NameHandler(Handler):
    """Handler that matches vector names exactly."""

    def __init__(self, name, key, successor=None):
        super().__init__(key, successor)
        self.name = name

    def handle(self, vector_name, data, data_organizer):
        if vector_name == self.name:
            data_organizer.data[self.key] = data
        elif self.successor:
            self.successor.handle(vector_name, data, data_organizer)


class TimeHandler(NameHandler):
    def __init__(self, key="time", successor=None):
        super().__init__("time", key, successor)


class FrequencyHandler(NameHandler):
    def __init__(self, key="frequency", successor=None):
        super().__init__("frequency", key, successor)


class HarmonicHandler(NameHandler):
    def __init__(self, key="harmonic", successor=None):
        super().__init__("harmonic", key, successor)
# >>>


# pattern handlers <<<
class PatternHandler(Handler):
    """Handler that matches vector names using a regex pattern."""

    def __init__(self, patterns, key, successor=None):
        super().__init__(key, successor)
        self.patterns = [re.compile(pattern) for pattern in patterns]

    @abstractmethod
    def process(self, match, vector_name, data, data_organizer):
        pass

    def handle(self, vector_name, data, data_organizer):
        match = False
        for pattern in self.patterns:
            match = pattern.match(vector_name)
            if match:
                self.process(match, vector_name, data, data_organizer)
                break
        if not match and self.successor:
            self.successor.handle(vector_name, data, data_organizer)


class PoleZeroHandler(PatternHandler):
    def __init__(self, key="pole_zero", successor=None):
        super().__init__([r"(pole|zero)\(\d+\)"], key, successor)

    def process(self, match, vector_name, data, data_organizer):
        data_organizer.data.setdefault(self.key, {})[vector_name] = data


class ImpedanceHandler(PatternHandler):
    def __init__(self, key="impedances", successor=None):
        super().__init__([r".*impedance.*"], key, successor)

    def process(self, match, vector_name, data, data_organizer):
        data_organizer.data.setdefault(self.key, {})[vector_name] = data


class TransferFunctionHandler(PatternHandler):
    def __init__(self, key="transfer_function", successor=None):
        super().__init__([r"Transfer_function"], key, successor)

    def process(self, match, vector_name, data, data_organizer):
        data_organizer.data[self.key] = data


class ParameterHandler(PatternHandler):
    def __init__(self, key="parameters", successor=None):
        super().__init__([r".*@\w+\[\w+\]$"], key, successor)

    def process(self, match, vector_name, data, data_organizer):
        clean_name = vector_name.replace("@", "")
        hierarchy = clean_name.split(".")
        d = data_organizer.data.setdefault(self.key, {})
        for level in hierarchy[:-1]:
            d = d.setdefault(level, {})
        d[hierarchy[-1]] = data


class CurrentHandler(PatternHandler):
    def __init__(self, key="currents", successor=None):
        super().__init__([r".*#branch.*$", r".*#flow.*$", r".*@\w+\[i\]$"], key, successor)

    def process(self, match, vector_name, data, data_organizer):
        clean_name = vector_name.replace("#branch", "")
        hierarchy = clean_name.split(".")
        d = data_organizer.data.setdefault(self.key, {})
        for level in hierarchy[:-1]:
            d = d.setdefault(level, {})
        d[hierarchy[-1]] = data
# >>>
