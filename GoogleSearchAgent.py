from agentDVerse.agent import Agent
from googleapiclient.discovery import build


class GoogleSearchAgent(Agent):
    def __init__(self, name="google_search",
                 description="Searches Google and returns top links",
                 api_key=None,
                 search_engine_id=None):
        """
        Initialize a GoogleSearchAgent
        Args:
            name (str, optional): Name of the agent. Defaults to "google_search".
            description (str, optional): Description of the agent. Defaults to "Searches Google and returns top links".
            api_key (str, optional): Your Google Custom Search API key. Defaults to None.
            search_engine_id (str, optional): Your Google Custom Search Engine ID. Defaults to None.
        """
        super().__init__(name, description, ["search"], "list")  # Handles "search" topic, outputs a list
        self.api_key = api_key
        self.search_engine_id = search_engine_id
        if not (api_key and search_engine_id):
            raise ValueError("Both API key and Search Engine ID are required for Google Search Agent")

        self.service = build("customsearch", "v1", developerKey=self.api_key)

    def callback(self, message):
        """
        Callback function to handle incoming messages.

        Args:
            message (dict[str, Any]): The message received from Kafka.
        """
        query = message.get("query")
        if query:
            results = self.search_google(query)
            self.send_response_to_next(message, results)

    def search_google(self, query):
        """
        Search Google using the Custom Search API and return the top 5 links.

        Args:
            query (str): The search query.

        Returns:
            dict: A dictionary containing a list of results under the key "search_results".
        """
        res = self.service.cse().list(
            q=query,
            cx=self.search_engine_id,
            num=5,  # Number of results to retrieve
        ).execute()
        return {"search_results": res['items']}