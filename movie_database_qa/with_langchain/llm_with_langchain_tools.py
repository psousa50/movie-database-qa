from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.tools.convert_to_openai import format_tool_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.agents import AgentExecutor
from langchain_openai import ChatOpenAI

from movie_database_qa.with_langchain.callbacks import LLMStartHandler


class LLMWithLangChainTools:
    def __init__(self, user_input, tools, system_prompt, options={}):
        client = ChatOpenAI(model="gpt-4", temperature=0)
        self.user_input = user_input
        self.agent_executor = self.create_agent_executor(client, tools, system_prompt)

    def create_agent_executor(self, client, tools, system_prompt):
        llm_with_tools = client.bind(
            functions=[format_tool_to_openai_function(t) for t in tools]
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    system_prompt,
                ),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_to_openai_function_messages(
                    x["intermediate_steps"]
                ),
            }
            | prompt
            | llm_with_tools
            | OpenAIFunctionsAgentOutputParser()
        )

        self.handler = LLMStartHandler()
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        return agent_executor

    def get_response(self):
        response = self.agent_executor.invoke(
            {"input": self.user_input}, config={"callbacks": [self.handler]}
        )
        return response
