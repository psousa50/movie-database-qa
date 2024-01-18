import sys
from llm_with_langchain_tools import (
    LLMWithLangChainTools,
    tools,
    system_prompt as langchain_system_prompt,
)
from llm_with_tools import (
    LLMWithTools,
    system_prompt as tools_system_prompt,
)
from tmdb_tools import tmdb_tools_map


def start(input):
    llm = LLMWithTools(input, tmdb_tools_map, tools_system_prompt)
    # llm = LLMWithLangChainTools(input, tools, langchain_system_prompt)
    response = llm.get_response()
    print("response", response)


if __name__ == "__main__":
    input = sys.argv[1]
    start(input)
