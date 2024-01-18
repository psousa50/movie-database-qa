from openai import OpenAI
from prompts import system_prompt
import sys
from math_tools import math_tools_map

from chat_bot import ChatBot


def start(input):
    client = OpenAI()
    chat_bot = ChatBot(client, input, math_tools_map, system_prompt)
    response = chat_bot.get_response()
    print("response", response)


if __name__ == "__main__":
    input = sys.argv[1]
    start(input)
