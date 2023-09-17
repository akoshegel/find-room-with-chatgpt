import logging
import json
from typing import List, Tuple, TypedDict

import openai

# create Preferences type alias
Preferences = List[Tuple[int, str]]


# create Advertisment type alias
class Advertisment(TypedDict):
    text: str
    link: str
    timestamp: int


# create ScoredAdvertisment type alias
class ChatGPTResponse(TypedDict):
    searcher_post: bool
    text: str
    timestamp: int
    link: str
    explanation: str
    score: int


# logger for chatgpt file
logger = logging.getLogger("chatgpt")


# chatgpt service, gets openai as dependency
class ChatGPT:
    # base messages that gives context for chatgpt
    __base_prompts = [
        # used to tell chatgpt the context and the role
        {"role": "system", "content": "You are a helpful assistant."},
    ]

    # constructor function sets openai as dependency
    def __init__(self, openai: openai):
        self.openai = openai

    # makes prompt for chatgpt from the text of the advertisment and user's preferences
    def __make_user_prompts(self, advertisment: Advertisment, preferences: Preferences):
        # generate bulletpoint list
        preferences_text = " ".join(
            f"<preference>{item[0]} {item[1]}</preference>" for item in preferences
        )
        return [
            {
                "role": "user",
                "content": "You will be given an advertisment about an available accomodation and you should decide on a 1 to 10 scale how well it fits my preferences. The advertisment will be provided in <advertisment> HTML tags as string and my preferences in <preferences> HTML tags each preferance seperated in a <preferance> tags. At the beginning of each <preference> HTML tag you will see a number from 1 to 3 showing how important it is for me. Return a JSON object with the link for the advertisment which can be founded in the <link> HTML tags and the score on how well it fits my preferences and your reasoning. Some of the advertisments are searcher posts from people who are searching for a room. Usually their posts starts with greetings. Add searcher_post key and true value to the json if you think it's from somebody who is searching for a room and false value if you think the post is a room advertisment. Don't generate long response just return the JSON object.",
            },
            {
                "role": "user",
                "content": f"<link>{advertisment['link']}</link><advertisment>{advertisment['text']}</advertisment><preferences>{preferences_text}</preferences>",
            },
        ]

    # extract data from chatgpt response
    def __format_chatgpt_response(self, response: dict) -> dict:
        # return parsed json response from chatgpt
        return json.loads(response["choices"][0]["message"]["content"])

    # rates accomodations with chatgpt
    def rate_advertisment(self, advertisment: Advertisment, preferences: Preferences):
        # create messages array
        messages = [
            *self.__base_prompts,
            *self.__make_user_prompts(advertisment, preferences),
        ]
        # send request to openai server
        response = self.openai.ChatCompletion.create(model="gpt-4", messages=messages)
        # format response
        return {
            "text": advertisment["text"],
            "timestamp": advertisment["timestamp"],
            **self.__format_chatgpt_response(response),
        }
