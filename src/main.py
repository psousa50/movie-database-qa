import sys
from math_tools import math_tools_map
from tmdb_tools import tmdb_tools_map
from llm_with_langchain_tools import LLMWithLangChainTools, tools, system_prompt
from llm_with_tools import LLMWithTools, system_prompt


def start(input):
    llm = LLMWithTools(input, tmdb_tools_map, system_prompt)
    # llm = LLMWithLangChainTools(input, tools, system_prompt)
    response = llm.get_response()
    print("response", response)


if __name__ == "__main__":
    input = sys.argv[1]
    start(input)
