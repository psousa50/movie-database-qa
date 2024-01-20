import textwrap
import requests


def tmdb_request(endpoint):
    url = f"https://api.themoviedb.org/3/{endpoint}"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0OGRiNmVlNjcwOTk2MTU4ZDdmYmM2MzYzOWUyNzQ5NyIsInN1YiI6IjY1YTUwMzQ1NjQ3NjU0MDEyMmQ2ZWNhZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.rvWFGrgGFsrLRXutKr6kXoSGKTbMQKr5ZVg65R_GhWc",
    }

    response = requests.get(url, headers=headers)

    return response.json()


def discover_movies(
    include_adult="",
    include_video="",
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
    query = textwrap.dedent(
        f"""\
            discover/movie?
            {add("include_adult", include_adult)}
            {add("include_video", include_video)}
            {add("language", language)}
            {add("primary_release_year", primary_release_year)}
            {add("region", region)}
            {add("sort_by", sort_by)}
            {add("vote_average", vote_average)}
            {add("vote_count", vote_count)}
            {add("watch_region", watch_region)}
            {add("with_cast", with_cast)}
            {add("with_companies", with_companies)}
            {add("with_crew", with_crew)}
            {add("with_genres", with_genres)}
            {add("with_keywords", with_keywords)}
            {add("with_origin_country", with_origin_country)}
            {add("with_original_language", with_original_language)}
            {add("with_people", with_people)}
            {add("without_companies", without_companies)}
            {add("without_genres", without_genres)}
            {add("without_keywords", without_keywords)}
            {add("without_watch_providers", without_watch_providers)}
            {add("year", year)}            
        """
    ).replace("\n", "")
    print("Discover query", query)
    response = tmdb_request(query)
    return [(movie["id"], movie["title"]) for movie in response["results"]]


def add(key, value):
    if value:
        return f"&{key}={value}"
    return ""


def search_movie(query: str):
    """Searches for a list of movies and returns the id and the title"""
    print("Search movie query", query)
    response = tmdb_request(
        f"search/movie?query={query}&include_adult=false&language=en-US&page=1"
    )
    return [(movie["id"], movie["title"]) for movie in response["results"]]


def search_person(query: str):
    """Searches for a list of people and returns the id and the name"""
    print("Search person query", query)
    response = tmdb_request(
        f"search/person?query={query}&include_adult=false&language=en-US&page=1"
    )
    return [
        (person["id"], person["name"], person["known_for_department"])
        for person in response["results"]
    ]


def get_movie_reviews(movie_id: int):
    """Gets the reviews for a movie"""
    print("Reviews query", movie_id)
    response = tmdb_request(f"movie/{movie_id}/reviews?language=en-US&page=1")
    return [review["content"] for review in response["results"]]


def get_movie_cast(movie_id: int):
    """Gets the cast for a movie"""
    print("Cast query", movie_id)
    response = tmdb_request(f"movie/{movie_id}/credits?language=en-US&page=1")
    only_acting_cast = [
        cast for cast in response["cast"] if cast["known_for_department"] == "Acting"
    ][:10]
    return [(cast["name"], cast["character"]) for cast in only_acting_cast]


def all_movie_genres():
    """Gets all movie genres"""
    response = tmdb_request(f"genre/movie/list")
    return response["genres"]
