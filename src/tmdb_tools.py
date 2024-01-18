import requests

from tool import Tool


def tmdb_request(endpoint):
    url = f"https://api.themoviedb.org/3/{endpoint}"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0OGRiNmVlNjcwOTk2MTU4ZDdmYmM2MzYzOWUyNzQ5NyIsInN1YiI6IjY1YTUwMzQ1NjQ3NjU0MDEyMmQ2ZWNhZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.rvWFGrgGFsrLRXutKr6kXoSGKTbMQKr5ZVg65R_GhWc",
    }

    response = requests.get(url, headers=headers)

    return response.json()


def discover_movies(
    include_adult=False,
    include_video=False,
    language="",
    primary_release_year="",
    region="",
    sort_by="",
    vote_average="",
    vote_count="",
    watch_region="",
    with_cast="",
    with_companies="",
    with_crew="",
    with_genres="",
    with_keywords="",
    with_origin_country="",
    with_original_language="",
    with_people="",
    without_companies="",
    without_genres="",
    without_keywords="",
    without_watch_providers="",
    year="",
):
    """Discovers movies"""
    response = tmdb_request("discover/movie?language=en-US&sort_by=popularity.desc")
    return [(movie["id"], movie["title"]) for movie in response["results"]]


def search_movie(query: str):
    """Searches for a list of movies and returns the id and the title"""
    response = tmdb_request(
        f"search/movie?query={query}&include_adult=false&language=en-US&page=1"
    )
    return [(movie["id"], movie["title"]) for movie in response["results"]]


def get_movie_reviews(movie_id: int):
    """Gets the reviews for a movie"""
    response = tmdb_request(f"movie/{movie_id}/reviews?language=en-US&page=1")
    return [review["content"] for review in response["results"]]


def get_movie_cast(movie_id: int):
    """Gets the cast for a movie"""
    response = tmdb_request(f"movie/{movie_id}/credits?language=en-US&page=1")
    return [(cast["name"], cast["character"]) for cast in response["cast"]]


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
