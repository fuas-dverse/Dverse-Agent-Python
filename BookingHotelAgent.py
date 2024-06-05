import requests
from nltk.downloader import download as nltk_download
from nltk.tag.perceptron import PerceptronTagger
from nltk.chunk import treebank_chunk_parser
from agentDVerse.agent import Agent

nltk_download('punkt')
nltk_download('averaged_perceptron_tagger')
nltk_download('maxent_treebank_pos_tagger')
nltk_download('words')
nltk_download('treebank')

tagger = PerceptronTagger()
locationtagger = treebank_chunk_parser(tagger)

booking_url:str="https://booking-com.p.rapidapi.com/v1/hotels"

class BookingHotelAgent(Agent):
    def __init__(self, name="booking_hotel", description="Searches hotels using Booking.com API"):
        """
        Initialize a BookingHotelAgent

        Args:
            name (str, optional): Name of the agent. Defaults to "booking_hotel".
            description (str, optional): Description of the agent. Defaults to "Searches hotels using Booking.com API".
        """
        super().__init__(name, description, ["search"], "list")  # Handles "search" topic, outputs a list

        self.headers = {
            "X-RapidAPI-Host": "booking-com.p.rapidapi.com",
            "X-RapidAPI-Key": "YOUR_API_KEY",  # Replace with the actual API key
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }

    def callback(self, message):
        """
        Callback function to handle incoming messages.

        Args:
            message (dict[str, Any]): The message received from Kafka.
        """
        user_input = message.get("query")
        if user_input:
            hotels = self.search_hotels(user_input)
            if hotels:
                self.send_response_to_next(message, hotels)
            else:
                self.send_response_to_next(message, {"message": "No hotels found for your search."})

    def search_hotels(self, user_input):
        """
        Search for hotels using Booking.com API based on user input.

        Args:
            user_input (str): User's search query.

        Returns:
            dict: A dictionary containing a list of hotels under the key "hotels" or an error message under "message".
        """
        city = locationtagger.find_locations(text=user_input.title()).cities[0] if locationtagger.find_locations(
            text=user_input.title()).cities else None
        if city:
            print(f"Searching hotels in {city}...")
            try:
                location_data = \
                requests.get(booking_url+"/locations", headers=self.headers,
                             params={"name": city, "locale": "en-gb"}).json()[0]
                hotels = requests.get(booking_url+"/search", headers=self.headers,
                                      params={
                                          "dest_id": location_data["dest_id"],
                                          "dest_type": location_data["dest_type"],
                                          "adults_number": "2",
                                          "checkin_date": "2024-09-14",
                                          "checkout_date": "2024-09-15",
                                          "order_by": "popularity",
                                          "filter_by_currency": "EUR",
                                          "room_number": "1",
                                          "locale": "en-gb",
                                          "units": "metric",
                                      }).json().get("result")[:3]
                return {"hotels": [{"name": hotel.get("hotel_name"), "address": hotel.get("address"),
                                    "rating": hotel.get("review_score_word"), "price": hotel.get("min_total_price"),
                                    "url": hotel.get("url"), "image": hotel.get("main_photo_url")} for hotel in hotels]}
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
                return {"message": "An error occurred while searching for hotels."}
        else:
            print("No city found in the input.")
            return {"message": "No city found in your search."}

