class Tool:
    def __init__(self, tool_name, parameters, description, fn):
        self.tool_name = tool_name
        self.parameters = parameters
        self.description = description
        self.fn = fn

    def __call__(self, parameters_values):
        return self.fn(**parameters_values)

    def __str__(self):
        return self.description

    def __repr__(self):
        return self.description

    def to_json(self):
        return {
            "tool_name": self.tool_name,
            "parameters": self.parameters,
            "description": self.description,
        }
