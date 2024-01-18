import json
from prompts import system_prompt


class ChatBot:
    def __init__(self, client, user_input, tools_map, system_prompt):
        self.client = client
        self.user_input = user_input
        self.tools_map = tools_map
        self.messages = []
        self.contextual_information = []

    def llm_response(self):
        tools = [tool.to_json() for tool in self.tools_map.values()]
        tools_json = json.dumps(tools, indent=4)
        contextual_information_json = json.dumps(self.contextual_information, indent=4)

        self.messages = []
        self.add_message(
            "system",
            system_prompt.replace("{tools}", tools_json).replace(
                "{contextual_information}", contextual_information_json
            ),
        )
        self.add_message("user", self.user_input)

        print("messages", self.messages)
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
                tool = self.tools_map[tool_name]
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
