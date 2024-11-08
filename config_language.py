import json
import re
import sys
import math

class ConfigLanguage:
    def __init__(self):
        self.variables = {}

    def parse_value(self, value, level=0):
        if isinstance(value, dict):
            return self.convert_dict(value, level)
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, str) and re.match(r"\[\^.*\]", value):
            return self.evaluate_expression(value[2:-1])
        elif isinstance(value, str):
            return value
        else:
            raise ValueError(f"Unsupported value type: {type(value)}")

    def convert_dict(self, data, level=1):
        indent = '  ' * level
        result = "{\n"
        for key, value in data.items():
            if not re.match(r"^[_A-Za-z][_a-zA-Z0-9]*$", key):
                raise ValueError(f"Invalid variable name: {key}")
            if isinstance(value, dict):
                result += f"{indent}{key} = {self.parse_value(value, level + 1)}\n"
            else:
                result += f"{indent}{key} = {self.parse_value(value, level)}\n"
        result += '  ' * (level - 1) + "}"
        return result

    def evaluate_expression(self, expr):
        expr = expr.strip()
        int_variables = {key: int(value) for key, value in self.variables.items()}
        try:
            allowed_globals = {"__builtins__": None, "math": math, "max": max, "sqrt": math.sqrt}
            result = eval(expr, allowed_globals, int_variables)
            return str(result)
        except Exception as e:
            raise ValueError(f"Error evaluating expression: {expr} ({e})")

    def define_variable(self, name, value):
        if not re.match(r"^[_A-Za-z][_a-zA-Z0-9]*$", name):
            raise ValueError(f"Invalid variable name: {name}")
        self.variables[name] = value
        return f"var {name} = {value}"

    def parse_json(self, data):
        output = ""
        for key, value in data.items():
            if isinstance(value, dict):
                output += f"var {key} = {self.convert_dict(value)}\n"
            else:
                output += f"{self.define_variable(key, self.parse_value(value))}\n"
        return output

def main():
    json_input = sys.stdin.read()
    data = json.loads(json_input)

    config_lang = ConfigLanguage()

    try:
        output = config_lang.parse_json(data)
        print(output)
    except ValueError as e:
        print(f"Syntax error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
