import sys

from with_langchain.llm_with_langchain_tools import LLMWithLangChainTools
from with_langchain.tmdb_tools import tools
from with_langchain.prompt import system_prompt as langchain_system_prompt

from from_scratch.llm_with_tools import LLMWithTools
from from_scratch.tmdb_tools import tmdb_tools_map
from from_scratch.prompt import system_prompt as tools_system_prompt


def start(llm_type, input):
    if llm_type == "1":
        llm = LLMWithTools(input, tmdb_tools_map, tools_system_prompt)
    elif llm_type == "2":
        llm = LLMWithLangChainTools(input, tools, langchain_system_prompt)
    else:
        raise ValueError(f"Unknown llm_type {llm_type}")
    # llm = LLMWithLangChainTools(input, tools, langchain_system_prompt)
    print(input)
    print("type:", llm_type)
    print(
        "=============================================================================="
    )
    print()
    response = llm.get_response()
    print(response)


if __name__ == "__main__":
    llm_type = sys.argv[1]
    input = sys.argv[2]
    start(llm_type, input)
