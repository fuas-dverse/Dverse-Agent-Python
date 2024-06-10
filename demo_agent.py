import time
from agentDVerse.agent import Agent


def callback(x):
    agent.send_response_to_next(
        initial=x,
        message={
            "message": "Hello, this is a demo agentDVerse.",
            "time": time.time()
        })


if __name__ == "__main__":
    agent = Agent(
        name="Hotel Agent",
        description="This is a agentDVerse that will provide information and book a hotel for you travels.",
        topics=["travel", "hotel", "booking", "vacation"],
        output_format="json",
        callback=callback
    )
