from movie_database_qa.tmdb_functions import (
    discover_movies,
    movie_cast,
    movie_reviews,
    movie_details,
    person_details,
    search_keyword,
    search_movie,
    search_person,
    all_movie_genres,
)

from movie_database_qa.from_scratch.tool import Tool


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
        "primary_release_date.gte": {
            "type": "date",
            "description": "primary release date greater than or equal to",
        },
        "primary_release_date.lte": {
            "type": "date",
            "description": "primary release date less than or equal to",
        },
        "region": {"type": "string", "description": "region"},
        "sort_by": {"type": "string", "description": "sort by"},
        "vote_average": {"type": "float", "description": "vote average"},
        "vote_count": {"type": "int", "description": "vote count"},
        "watch_region": {"type": "string", "description": "watch region"},
        "with_cast": {
            "type": "int",
            "description": "list of person ids, NOT names, use comma (,) for AND and pipe (|) for OR",
        },
        "with_companies": {
            "type": "int",
            "description": "list of company ids, NOT names, use comma (,) for AND and pipe (|) for OR",
        },
        "with_crew": {
            "type": "int",
            "description": "list of person ids, NOT names, use comma (,) for AND and pipe (|) for OR",
        },
        "with_genres": {
            "type": "int",
            "description": "list of genre ids, NOT names, use comma (,) for AND and pipe (|) for OR",
        },
        "with_keywords": {
            "type": "int",
            "description": "list of keyword ids, NOT names, use comma (,) for AND and pipe (|) for OR",
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
            "type": "int",
            "description": "list of person ids, NOT names, use comma (,) for AND and pipe (|) for OR",
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
    returned_fields=["id", "title", "overview"],
    fn=discover_movies,
)


search_movie_tool = Tool(
    tool_name="search_movie",
    parameters={"query": {"type": "string", "description": "query to search"}},
    description=search_movie.__doc__,
    returned_fields=["id", "title", "overview", "genres"],
    fn=search_movie,
)

search_person_tool = Tool(
    tool_name="search_person",
    parameters={"query": {"type": "string", "description": "query to search"}},
    description=search_person.__doc__,
    returned_fields=["id", "name", "known_for_department"],
    fn=search_person,
)

search_keyword_tool = Tool(
    tool_name="search_keyword",
    parameters={"query": {"type": "string", "description": "query to search"}},
    description=search_keyword.__doc__,
    returned_fields=["id", "name"],
    fn=search_keyword,
)

movie_details_tool = Tool(
    tool_name="movie_details",
    parameters={"movie_id": {"type": "int", "description": "movie id"}},
    description=movie_details.__doc__,
    returned_fields=[
        "id"
        "title"
        "overview"
        "genres"
        "release_date"
        "runtime"
        "vote_average"
        "vote_count"
        "poster_path"
    ],
    fn=movie_details,
)

movie_reviews_tool = Tool(
    tool_name="movie_reviews",
    parameters={"movie_id": {"type": "int", "description": "movie id"}},
    description=movie_reviews.__doc__,
    returned_fields=["content"],
    fn=movie_reviews,
)

movie_cast_tool = Tool(
    tool_name="movie_cast",
    parameters={"movie_id": {"type": "int", "description": "movie id"}},
    description=movie_cast.__doc__,
    returned_fields=["id", "name", "character"],
    fn=movie_cast,
)

person_details_tool = Tool(
    tool_name="person_details",
    parameters={"person_id": {"type": "int", "description": "person id"}},
    description=person_details.__doc__,
    returned_fields=[
        "id" "name" "known_for_department" "birthday" "deathday" "place_of_birth"
    ],
    fn=person_details,
)

all_movie_genres_tool = Tool(
    tool_name="all_movie_genres",
    parameters={},
    description=all_movie_genres.__doc__,
    returned_fields=["id", "name"],
    fn=all_movie_genres,
)


tmdb_tools_map = {
    tool.tool_name: tool
    for tool in [
        discover_movies_tool,
        search_movie_tool,
        search_person_tool,
        search_keyword_tool,
        movie_details_tool,
        movie_reviews_tool,
        movie_cast_tool,
        person_details_tool,
        all_movie_genres_tool,
    ]
}
