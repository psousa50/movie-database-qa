from openai import OpenAI
from prompts import system_prompt
import sys
from math_tools import math_tools_map
from tmdb_tools import tmdb_tools_map

from llm_with_tools import LLMWithTools


def start(input):
    client = OpenAI()
    llm = LLMWithTools(client, input, tmdb_tools_map, system_prompt)
    response = llm.get_response()
    print("response", response)


if __name__ == "__main__":
    input = sys.argv[1]
    start(input)
