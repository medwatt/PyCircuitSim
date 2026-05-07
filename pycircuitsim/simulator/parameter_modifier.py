class ParameterModifier:
    def __init__(self, hierarchical_name: tuple, parameter_changes: dict):
        self.hierarchical_name = hierarchical_name
        self.parameter_changes = parameter_changes

    def get_alter_commands(self) -> str:
        """
        Builds .alter commands for the parameter changes.
        """
        path_str = ".".join(self.hierarchical_name)
        commands = []
        for key, value in self.parameter_changes.items():
            commands.append(f"alter @{key[0]}.{path_str}.{key}={value}")
        return "\n".join(commands)
