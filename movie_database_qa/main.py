import json
import sys

from movie_database_qa.from_scratch.llm_with_tools import LLMWithTools
from movie_database_qa.from_scratch.prompt import system_prompt as tools_system_prompt
from movie_database_qa.from_scratch.tmdb_tools import tmdb_tools_map
from movie_database_qa.log import log, setup_log
from movie_database_qa.with_langchain.llm_with_langchain_tools import (
    LLMWithLangChainTools,
)
from movie_database_qa.with_langchain.prompt import (
    system_prompt as langchain_system_prompt,
)
from movie_database_qa.with_langchain.tmdb_tools import tools


def start(llm_type, user_input):
    options = {"verbose": True}
    if llm_type == "1":
        llm = LLMWithTools(user_input, tmdb_tools_map, tools_system_prompt, options)
    elif llm_type == "2":
        llm = LLMWithLangChainTools(user_input, tools, langchain_system_prompt, options)
    else:
        raise ValueError(f"Unknown llm_type {llm_type}")
    # llm = LLMWithLangChainTools(input, tools, langchain_system_prompt)
    log(user_input)
    log(f"type: {llm_type}")
    log(
        "=============================================================================="
    )
    log()
    response = llm.get_response()
    log(response)


if __name__ == "__main__":
    llm_type = sys.argv[1]
    user_input = sys.argv[2]
    options = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
    setup_log(options)
    start(llm_type, user_input)
