import json

from openai import OpenAI

from movie_database_qa.log import log_if, verbose


class LLMWithTools:
    def __init__(self, user_input, tools_map, system_prompt, options={}):
        self.client = OpenAI()
        self.user_input = user_input
        self.tools_map = tools_map
        self.system_prompt = system_prompt
        self.messages = []
        self.contextual_information = []
        self.options = options

    def llm_response(self):
        tools = [tool.to_json() for tool in self.tools_map.values()]
        tools_json = json.dumps(tools, indent=4)
        contextual_information_json = json.dumps(self.contextual_information, indent=4)

        self.messages = []
        self.add_message(
            "system",
            self.system_prompt.replace("{tools}", tools_json).replace(
                "{contextual_information}", contextual_information_json
            ),
        )
        self.add_message("user", self.user_input)

        log_if(
            "prompts",
            "==============================================================================\n",
            json.dumps(self.messages, indent=4)
            .replace("\\n", "\n")
            .replace('\\"', '"'),
            "------------------------------------------------------------------------------\n",
        )
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=self.messages,
            temperature=0.0,
        )
        llm_response = response.choices[0].message.content
        verbose("Response", llm_response)
        return json.loads(llm_response)

    def build_tools_prompt(self, tools):
        tools_json = [self.create_tool_json(tool) for tool in tools]
        tools_prompt = json.dumps(tools_json, indent=4)
        return tools_prompt

    def create_tool_json(self, tool):
        return {
            "tool": tool.tool_name,
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
                returned_fields_to_include = llm_response["returned_fields_to_include"]

                if isinstance(tool_response, dict):
                    tool_response_filtered = {
                        k: v
                        for k, v in tool_response.items()
                        if k in returned_fields_to_include
                    }
                else:
                    tool_response_filtered = [
                        {k: v for k, v in r.items() if k in returned_fields_to_include}
                        for r in tool_response
                    ]
                verbose(
                    "Tool response filtered",
                    json.dumps(tool_response_filtered, indent=4),
                )
                self.contextual_information.append(
                    {
                        "tool": tool_name,
                        "parameters": parameters,
                        "response": tool_response_filtered,
                    }
                )
        return response
