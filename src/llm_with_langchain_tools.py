from langchain.agents import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.tools.convert_to_openai import format_tool_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.agents import AgentExecutor
from langchain_openai import ChatOpenAI

from tmdb_tools import tmdb_request


@tool
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
    query = f"""discover/movie?
            include_adult={include_adult}&
            include_video={include_video}&
            {add("language", language)}&
            {add("primary_release_year", primary_release_year)}&
            {add("region", region)}&
            {add("sort_by", sort_by)}&
            {add("vote_average", vote_average)}&
            {add("vote_count", vote_count)}&
            {add("watch_region", watch_region)}&
            {add("with_cast", with_cast)}&
            {add("with_companies", with_companies)}&
            {add("with_crew", with_crew)}&
            {add("with_genres", with_genres)}&
            {add("with_keywords", with_keywords)}&
            {add("with_origin_country", with_origin_country)}&
            {add("with_original_language", with_original_language)}&
            {add("with_people", with_people)}&
            {add("without_companies", without_companies)}&
            {add("without_genres", without_genres)}&
            {add("without_keywords", without_keywords)}&
            {add("without_watch_providers", without_watch_providers)}&
            {add("year", year)}            
        """
    print("query", query)
    response = tmdb_request(query)
    return [(movie["id"], movie["title"]) for movie in response["results"]]


def add(key, value):
    if value:
        return f"{key}={value}&"
    return ""


class LLMWithLangChainTools:
    def __init__(self, user_input, tools, system_prompt):
        client = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        self.user_input = user_input
        self.agent_executor = self.create_agent_executor(client, tools, system_prompt)

    def create_agent_executor(client, tools, system_prompt):
        llm_with_tools = client.bind(
            functions=[format_tool_to_openai_function(t) for t in tools]
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    system_prompt,
                ),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_to_openai_function_messages(
                    x["intermediate_steps"]
                ),
            }
            | prompt
            | llm_with_tools
            | OpenAIFunctionsAgentOutputParser()
        )

        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        return agent_executor

    def get_response(self):
        response = self.agent_executor.invoke({"input": self.user_input})
        return response


tools = [discover_movies]

system_prompt = "You are a movie very helpful assistant that can help finding information movies. If a search for a movie returns more than one you should ask the suer for the one that he wants."
