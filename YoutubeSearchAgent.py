from agentDVerse.agent import Agent
from googleapiclient.discovery import build


class YoutubeSearchAgent(Agent):
    def __init__(self, name="youtube_search", description="Searches YouTube and returns top videos", api_key=None):
        """
        Initialize a YoutubeSearchAgent

        Args:
            name (str, optional): Name of the agent. Defaults to "youtube_search".
            description (str, optional): Description of the agent.
            Defaults to "Searches YouTube and returns top videos".
            api_key (str, optional): Your YouTube Data API v3 key. Defaults to None.
        """
        super().__init__(name, description, ["search"], "list")  # Handles "search" topic, outputs a list
        self.api_key = api_key
        if not self.api_key:
            raise ValueError("API key is required for Youtube Search Agent")

        self.service = build("youtube", "v3", developerKey=self.api_key)

    def callback(self, message):
        """
        Callback function to handle incoming messages.

        Args:
            message (dict[str, Any]): The message received from Kafka.
        """
        query = message.get("query")
        if query:
            results = self.search_youtube(query)
            self.send_response_to_next(message, results)

    def search_youtube(self, query):
        """
        Search YouTube using the YouTube Data API v3 and return the top 5 videos.

        Args:
            query (str): The search query.

        Returns:
            dict: A dictionary containing a list of videos under the key "search_results".
        """
        request = self.service.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=5  # Number of results to retrieve
        ).execute()
        return {"search_results": request["items"]}

