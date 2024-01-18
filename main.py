from openai import OpenAI
import sys
import json
import math

# import gradio as gr

system_prompt = """
You are a powerfull AI assistant. Your job is to answer questions from users.
You have a list of tools that you should use to answer questions. Don't use your own knowledge to answer questions. You know nothing about math.
If you need to use a tool, return a response in the following JSON format:
{
    "tool": "tool_name",
    "parameters": {
        "parameter_name": "parameter_value"
    }
}

Use the information returned by tools to answer the user's questions.

As soon as you are able to answer the user's question, return a response in the following JSON format:
{
    "tool": "none",
    "response: <your response>"
}

The tools are described below with the following schema:
{
    "tool_name": {
        "parameters": {
            "parameter_name": "parameter_type"
        },
        "description": "tool_description"
    }
}

Do not include code fences in your response, for example

    Bad response (because it contains the code fence):
    ```javascript
    console.log("hello world")
    ```

    Good response (because it only contains the code):
    console.log("hello world")


TOOLS:
{tools}

The responses returned by tools are described below. Please use them to answer the user's questions.

CONTEXTUAL INFORMATION:
{contextual_information}

"""


class ChatBot:
    def __init__(self, client, user_input, tools_map, system_prompt):
        self.client = client
        self.user_input = user_input
        tools = [tool.to_json() for tool in tools_map.values()]
        self.tools_json = json.dumps(tools, indent=4)
        self.messages = []
        self.contextual_information = []

    def llm_response(self):
        self.messages = []
        contextual_information_json = json.dumps(self.contextual_information, indent=4)
        self.add_message(
            "system",
            system_prompt.replace("{tools}", self.tools_json).replace(
                "{contextual_information}", contextual_information_json
            ),
        )
        self.add_message("user", input)

        print(
            "==============================================================================\n",
            json.dumps(self.messages, indent=4).replace("\\n", "\n").replace('"', '"'),
            "------------------------------------------------------------------------------\n",
        )
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=self.messages,
        )
        content = response.choices[0].message.content
        print("content", content)
        return json.loads(content)

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

    def get_response(self):
        response = None
        while response is None:
            llm_response = self.llm_response()
            tool_name = llm_response["tool"]
            if tool_name == "none":
                response = llm_response["response"]
            else:
                tool = tools_map[tool_name]
                parameters = llm_response["parameters"]
                tool_response = tool(parameters)
                self.contextual_information.append(
                    {
                        "tool_name": tool_name,
                        "parameters": parameters,
                        "response": tool_response,
                    }
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


def start(input):
    client = OpenAI()
    chat_bot = ChatBot(client, input, tools_map, system_prompt)
    response = chat_bot.get_response()
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
