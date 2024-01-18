from tmdb_functions import (
    discover_movies,
    get_movie_cast,
    get_movie_reviews,
    search_movie,
)

from tool import Tool


discover_movies_tool = Tool(
    tool_name="discover_movies",
    parameters={
        "include_adult": {"type": "bool", "description": "include adult movies"},
        "include_video": {"type": "bool", "description": "include video movies"},
        "language": {"type": "string", "description": "language"},
        "primary_release_year": {
            "type": "int",
            "description": "primary release year",
        },
        "region": {"type": "string", "description": "region"},
        "sort_by": {"type": "string", "description": "sort by"},
        "vote_average": {"type": "float", "description": "vote average"},
        "vote_count": {"type": "int", "description": "vote count"},
        "watch_region": {"type": "string", "description": "watch region"},
        "with_cast": {
            "type": "string",
            "description": "with cast, can be a comma (AND) or pipe (OR) separated query",
        },
        "with_companies": {
            "type": "string",
            "description": "with companies, can be a comma (AND) or pipe (OR) separated query",
        },
        "with_crew": {
            "type": "string",
            "description": "with crew, can be a comma (AND) or pipe (OR) separated query",
        },
        "with_genres": {
            "type": "string",
            "description": "with genres, can be a comma (AND) or pipe (OR) separated query",
        },
        "with_keywords": {
            "type": "string",
            "description": "with keywords, can be a comma (AND) or pipe (OR) separated query",
        },
        "with_origin_country": {
            "type": "string",
            "description": "with origin country",
        },
        "with_original_language": {
            "type": "string",
            "description": "with original language",
        },
        "with_people": {
            "type": "string",
            "description": "with people, can be a comma (AND) or pipe (OR) separated query",
        },
        "without_companies": {"type": "string", "description": "without companies"},
        "without_genres": {"type": "string", "description": "without genres"},
        "without_keywords": {"type": "string", "description": "without keywords"},
        "without_watch_providers": {
            "type": "string",
            "description": "without watch providers",
        },
        "year": {"type": "int", "description": "year"},
    },
    description=discover_movies.__doc__,
    fn=discover_movies,
)


search_movie_tool = Tool(
    tool_name="search_movie",
    parameters={"query": {"type": "string", "description": "query to search"}},
    description=search_movie.__doc__,
    fn=search_movie,
)

get_movie_reviews_tool = Tool(
    tool_name="get_movie_reviews",
    parameters={"movie_id": {"type": "int", "description": "movie id"}},
    description=get_movie_reviews.__doc__,
    fn=get_movie_reviews,
)

get_movie_cast_tool = Tool(
    tool_name="get_movie_cast",
    parameters={"movie_id": {"type": "int", "description": "movie id"}},
    description=get_movie_cast.__doc__,
    fn=get_movie_cast,
)


tmdb_tools_map = {
    tool.tool_name: tool
    for tool in [
        discover_movies_tool,
        search_movie_tool,
        get_movie_reviews_tool,
        get_movie_cast_tool,
    ]
}
