import math

from tool import Tool


def add_numbers(n1: int, n2: int):
    print("TOOL: add_numbers", n1, n2)
    return n1 + n2


def square_root_number(n: int):
    print("TOOL: square_root_number", n)
    return math.sqrt(n)


add_numbers_tool = Tool(
    tool_name="add_numbers",
    parameters={"n1": "int", "n2": "int"},
    description="add two numbers",
    fn=add_numbers,
)

square_root_number_tool = Tool(
    tool_name="square_root_number",
    parameters={"n": "int"},
    description="Take the square root of a number",
    fn=square_root_number,
)

math_tools_map = {
    tool.tool_name: tool for tool in [add_numbers_tool, square_root_number_tool]
}
