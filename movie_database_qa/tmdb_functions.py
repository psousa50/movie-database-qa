import textwrap
import requests

from movie_database_qa.log import log_if


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
    primary_release_date_gte="",
    primary_release_date_lte="",
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
            {add("primary_release_date.gte", primary_release_date_gte)}
            {add("primary_release_date.lte", primary_release_date_lte)}
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
    log_tool_query("Discover", query)
    response = tmdb_request(query)
    filtered_response = [
        {"id": movie["id"], "title": movie["title"], "overview": movie["overview"]}
        for movie in response["results"]
    ]
    log_tool_response("Response", filtered_response)
    return filtered_response


def add(key, value):
    if value:
        return f"&{key}={value}"
    return ""


def search_movie(query: str):
    """Searches for a list of movies by name, returns id and other information"""
    log_tool_query("Search movie", query)
    response = tmdb_request(
        f"search/movie?query={query}&include_adult=false&language=en-US&page=1"
    )
    filtered_response = [
        {"id": movie["id"], "title": movie["title"], "overview": movie["overview"]}
        for movie in response["results"]
    ]
    log_tool_response("Response", filtered_response)
    return filtered_response


def search_person(query: str):
    """Searches for a list of people by name, returns id and other information"""
    log_tool_query("Search person", query)
    response = tmdb_request(
        f"search/person?query={query}&include_adult=false&language=en-US&page=1"
    )
    filtered_response = [
        {
            "id": person["id"],
            "name": person["name"],
            "known_for_department": person["known_for_department"],
        }
        for person in response["results"]
    ]
    log_tool_response("Response", filtered_response)
    return filtered_response


def search_keyword(query: str):
    """Searches for a list of keywords by name, returns id and other information"""
    log_tool_query("Search keyword", query)
    response = tmdb_request(
        f"search/keyword?query={query}&include_adult=false&language=en-US&page=1"
    )
    filtered_response = [
        {
            "id": keyword["id"],
            "name": keyword["name"],
        }
        for keyword in response["results"]
    ]
    log_tool_response("Response", filtered_response)
    return filtered_response


def movie_details(movie_id: int):
    """Gets the details for a movie"""
    log_tool_query("Movie details", movie_id)
    response = tmdb_request(f"movie/{movie_id}?language=en-US")
    filtered_response = {
        "id": response["id"],
        "title": response["title"],
        "overview": response["overview"],
        "genres": response["genres"],
        "release_date": response["release_date"],
        "runtime": response["runtime"],
        "vote_average": response["vote_average"],
        "vote_count": response["vote_count"],
        "poster_path": response["poster_path"],
    }
    log_tool_response("Response", filtered_response)
    return filtered_response


def movie_reviews(movie_id: int):
    """Gets the reviews for a movie"""
    log_tool_query("Movie reviews", movie_id)
    response = tmdb_request(f"movie/{movie_id}/reviews?language=en-US&page=1")
    filtered_response = [
        {"content": review["content"]} for review in response["results"]
    ]
    log_tool_response("Response", filtered_response)
    return filtered_response


def movie_cast(movie_id: int):
    """Gets the cast for a movie"""
    log_tool_query("Movie cast", movie_id)
    response = tmdb_request(f"movie/{movie_id}/credits?language=en-US&page=1")
    only_acting_cast = [
        cast for cast in response["cast"] if cast["known_for_department"] == "Acting"
    ][:10]
    filtered_response = [
        {"id": cast["id"], "name": cast["name"], "character": cast["character"]}
        for cast in only_acting_cast
    ]
    log_tool_response("Response", filtered_response)
    return filtered_response


def person_details(person_id: int):
    """Gets a person details"""
    log_tool_query("Person details", person_id)
    response = tmdb_request(f"person/{person_id}?language=en-US")
    filtered_response = {
        "id": response["id"],
        "name": response["name"],
        "known_for_department": response["known_for_department"],
        "birthday": response["birthday"],
        "deathday": response["deathday"],
        "place_of_birth": response["place_of_birth"],
    }
    log_tool_response("Response", filtered_response)
    return filtered_response


def all_movie_genres():
    """Gets all movie genres"""
    log_tool_query("Movie genres")
    response = tmdb_request(f"genre/movie/list")
    filtered_response = {"genres": response["genres"]}
    log_tool_response("Response", filtered_response)
    return filtered_response


def log_tool_query(*args):
    log_if("tools_query", *args)


def log_tool_response(*args):
    log_if("tools_response", *args)
