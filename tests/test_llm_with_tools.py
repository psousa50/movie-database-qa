import unittest
from unittest.mock import Mock

from movie_database_qa.from_scratch.llm_with_tools import LLMWithTools
from movie_database_qa.from_scratch.tmdb_tools import tmdb_tools_map
from movie_database_qa.from_scratch.prompt import system_prompt as tools_system_prompt
from movie_database_qa.from_scratch.tool import Tool


class TestLLMWithTools(unittest.TestCase):
    def test_movie_name(self):
        tmdb_tools_map_mock = build_tools_mock()
        user_input = "Who is the main actor in the movie Die Hard?"
        llm = LLMWithTools(user_input, tmdb_tools_map_mock, tools_system_prompt)
        llm.get_response()
        tmdb_tools_map_mock["search_movie"].fn.assert_called_with(query="Die Hard")

    def test_actor_and_keywords(self):
        tmdb_tools_map_mock = build_tools_mock()
        user_input = "Find me a movie with Richard Gere that's about a navy pilot"
        llm = LLMWithTools(user_input, tmdb_tools_map_mock, tools_system_prompt)
        llm.get_response()
        tmdb_tools_map_mock["search_person"].fn.assert_called_with(query="Richard Gere")
        tmdb_tools_map_mock["discover_movies"].fn.assert_called_with(
            with_cast=1205, with_keywords="navy pilot"
        )


if __name__ == "__main__":
    unittest.main()


def build_tools_mock():
    return {
        tool_name: Tool(
            tool_name=tool_name,
            parameters=tool.parameters,
            returned_fields=tool.returned_fields,
            description=tool.description,
            fn=Mock(wraps=tool.fn),
        )
        for tool_name, tool in tmdb_tools_map.items()
    }
