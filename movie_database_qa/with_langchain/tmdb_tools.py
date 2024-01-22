from langchain.agents import tool

from movie_database_qa.tmdb_functions import (
    all_movie_genres,
    discover_movies,
    movie_cast,
    movie_reviews,
    search_movie,
    search_person,
)


@tool
def discover_movies_as_tool(
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
    return discover_movies(
        include_adult=include_adult,
        include_video=include_video,
        language=language,
        primary_release_year=primary_release_year,
        region=region,
        sort_by=sort_by,
        vote_average=vote_average,
        vote_count=vote_count,
        watch_region=watch_region,
        with_cast=with_cast,
        with_companies=with_companies,
        with_crew=with_crew,
        with_genres=with_genres,
        with_keywords=with_keywords,
        with_origin_country=with_origin_country,
        with_original_language=with_original_language,
        with_people=with_people,
        without_companies=without_companies,
        without_genres=without_genres,
        without_keywords=without_keywords,
        without_watch_providers=without_watch_providers,
        year=year,
    )


@tool
def search_movie_tool(query: str):
    """Searches movies"""
    return search_movie(query=query)


@tool
def search_person_tool(query: str):
    """Searches people"""
    return search_person(query=query)


@tool
def get_movie_reviews_tool(movie_id: int):
    """Gets movie reviews"""
    return movie_reviews(movie_id=movie_id)


@tool
def get_movie_cast_tool(movie_id: int):
    """Gets movie cast"""
    return movie_cast(movie_id=movie_id)


@tool
def all_movie_genres_tool():
    """Gets all movie genres"""
    return all_movie_genres()


tools = [
    discover_movies_as_tool,
    search_movie_tool,
    search_person_tool,
    get_movie_reviews_tool,
    get_movie_cast_tool,
    all_movie_genres_tool,
]
