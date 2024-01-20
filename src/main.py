import sys
from log import log

from with_langchain.llm_with_langchain_tools import LLMWithLangChainTools
from with_langchain.tmdb_tools import tools
from with_langchain.prompt import system_prompt as langchain_system_prompt

from from_scratch.llm_with_tools import LLMWithTools
from from_scratch.tmdb_tools import tmdb_tools_map
from from_scratch.prompt import system_prompt as tools_system_prompt


def start(llm_type, input):
    options = {"verbose": True}
    if llm_type == "1":
        llm = LLMWithTools(input, tmdb_tools_map, tools_system_prompt, options)
    elif llm_type == "2":
        llm = LLMWithLangChainTools(input, tools, langchain_system_prompt, options)
    else:
        raise ValueError(f"Unknown llm_type {llm_type}")
    # llm = LLMWithLangChainTools(input, tools, langchain_system_prompt)
    log(input)
    log(f"type: {llm_type}")
    log(
        "=============================================================================="
    )
    log()
    response = llm.get_response()
    log(response)


if __name__ == "__main__":
    llm_type = sys.argv[1]
    input = sys.argv[2]
    start(llm_type, input)
