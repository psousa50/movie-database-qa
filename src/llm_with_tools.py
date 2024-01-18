import json

from openai import OpenAI


class LLMWithTools:
    def __init__(self, user_input, tools_map, system_prompt):
        self.client = OpenAI()
        self.user_input = user_input
        self.tools_map = tools_map
        self.system_prompt = system_prompt
        self.messages = []
        self.contextual_information = []

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

        print(
            "==============================================================================\n",
            json.dumps(self.messages, indent=4)
            .replace("\\n", "\n")
            .replace('\\"', '"'),
            "------------------------------------------------------------------------------\n",
        )
        response = self.client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=self.messages,
            temperature=0.0,
        )
        llm_response = response.choices[0].message.content
        print("Response", llm_response)
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
                self.contextual_information.append(
                    {
                        "tool": tool_name,
                        "parameters": parameters,
                        "response": tool_response,
                    }
                )
        return response


system_prompt = """
You are a powerfull AI assistant. Your job is to answer questions from users.
You have a list of tools that you should use to answer questions.
If you need to use a tool, return a response in the following JSON format:
{
    "tool": "tool_name",
    "parameters": {
        "parameter_name": "parameter_value"
    }
}

You should include only the required parameters to answer the user's question. If the parameter is not required, you can omit it.

Use the information returned by tools to answer the user's questions.

As soon as you are able to answer the user's question, return a response in the following JSON format:
{
    "tool": "none",
    "response: <your response to the user's question>"
}

The tools are described below with the following schema:
{
    "tool": {
        "parameters": {
            "parameter_name": {
                "type": "parameter_type",
                "description": "parameter_description"
            }
        },
        "description": "tool_description"
    }
}

Do not include code fences in your response, for example:

    Bad response (because it contains the code fence):
    ```json
    {
        "tool": "none",
        "response": ...
    }
    ```

    Good response (because it only contains the json):
    {
        "tool": "none",
        "response": ...
    }

If the response contains a tool_name, it must include the parameters, otherwise the tool should be "none".

    Bad Response:
    {
        "tool": "tool_name",
        "response": "the final response"
    }

    Good response
    {
        "tool": "none",
        "response": "the final response"
    }

The CONTEXTUAL INFORMATION section contains the tools called with their parameters and the response returned by the tool. Use this information to answer the user's questions.
IMPORTANT: DON'T RETURN THE SAME TOOL TWICE.
The schema for the contextual information is:
{
    "tool": {
        "parameters": {
            "parameter_name": "parameter_value"
        },
        "response": "response"
    }
}


    
TOOLS:
{tools}

CONTEXTUAL INFORMATION:
{contextual_information}

"""
