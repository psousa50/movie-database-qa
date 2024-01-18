from openai import OpenAI
import sys
import json
import math

# import gradio as gr

system_prompt = """
You are a powerfull AI assistant. Your job is to answer questions from users.
You have a list of tools that you should use to answer questions.
If you need to use a tool, return a response in the following JSON format:
[
    {
        "tool": "tool_name",
        "parameters": {
            "parameter_name": "parameter_value",
        },
    {
        "tool": "another_tool_name",
        "parameters": {
            "parameter_name": "parameter_value",
        },
    }
]

You may nned to use multiple tools to answer a question. In that case, return a response in the following JSON format:

Use the information returned by tools to answer the user's questions.

As soon as you are able to answer the user's question, return a response in the following JSON format:
[
    {
        "tool": "none",
        "response: <your response>"
    }
]

The tools are described below with the following schema:
{
    "tool_name": {
        "parameters": {
            "parameter_name": "parameter_type"
        },
        "description": "tool_description"
    }
}

RETURN ONLY A VALID JSON STRING, NOTHING ELSE. Remove any characters that are not part of the JSON.

TOOLS:
{tools}

"""

ensure_json_prompt = """
You are a JSON expert. Fix the following JSON string so that it is valid JSON. If the JSON in envolved in ``` characters, remove them.

{json_string}
"""


class ChatBot:
    def __init__(self, client, tools_map, system_prompt):
        tools = [tool.to_json() for tool in tools_map.values()]
        tools_json = json.dumps(tools, indent=4)
        self.messages = []
        self.add_message("system", system_prompt.replace("{tools}", tools_json))
        self.client = client

    def fix_json(self, json_string):
        message = self.create_message(
            "system", ensure_json_prompt.replace("{json_string}", json_string)
        )
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[message],
        )
        return response.choices[0].message.content

    def llm_response(self):
        print(
            "==============================================================================\n",
            json.dumps(self.messages, indent=4).replace("\\n", "\n").replace('"', '"'),
            "------------------------------------------------------------------------------\n",
        )
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=self.messages,
        )
        content = response.choices[0].message.content
        print("content", content)
        fixed_json = self.fix_json(content)
        print("fixed_json", fixed_json)
        return json.loads(fixed_json)

    def build_tools_prompt(self, tools):
        tools_json = [self.create_tool_json(tool) for tool in tools]
        tools_prompt = json.dumps(tools_json, indent=4)
        return tools_prompt

    def create_tool_json(self, tool):
        return {
            "tool_name": tool.tool_name,
            "parameters": tool.parameters,
            "description": tool.description,
        }

    def add_message(self, role, content):
        self.messages.append(self.create_message(role, content))

    def create_message(self, role, content):
        return {"role": role, "content": content}

    def get_response(self, input):
        self.add_message("user", input)
        response = None
        while response is None:
            llm_response = self.llm_response()
            for tool_response in llm_response:
                tool_name = tool_response["tool"]
                if tool_name == "none":
                    response = tool_response["response"]
                else:
                    tool = tools_map[tool_name]
                    parameters = tool_response["parameters"]
                    tool_response = tool(parameters)
                    chat_bot.add_message(
                        "assistant",
                        f"{tool_name} {parameters} Response: {tool_response}",
                    )
        return response


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

tools_map = {
    tool.tool_name: tool for tool in [add_numbers_tool, square_root_number_tool]
}
client = OpenAI()
chat_bot = ChatBot(client, tools_map, system_prompt)


def start(input):
    response = chat_bot.get_response(input)
    print("response", response)


# def start_ui():
#     iface = gr.Interface(
#         fn=chat_bot.llm_response,
#         inputs=gr.Textbox(lines=2, placeholder="Type something..."),
#         outputs="text",
#         title="Simple Chatbot",
#         description="Type a message and get a response.",
#         layout="vertical",
#     )

#     iface.launch()


if __name__ == "__main__":
    input = sys.argv[1]
    start(input)
