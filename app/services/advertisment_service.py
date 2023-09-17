import logging
from typing import TypedDict, List

from app.domain.facebook_groups_scraper import FacebookGroupsScraper
from app.domain.chatgpt import ChatGPT, Preferences

logger = logging.getLogger(name="advertisment_service")


class AdvertismentService:
    def __init__(self, scraper: FacebookGroupsScraper, chatGPT: ChatGPT):
        self.scraper = scraper
        self.chatGPT = chatGPT

    # gets user's groups later from db
    def __get_groups(self, user_id: int) -> list[int]:
        return ["914912568563514"]

    # gets user's preferences later from db
    def __get_preferences(self, user_id: int) -> Preferences:
        return [[3, "CPR number registration"], [1, "at least 10 squaremeter room"]]

    # scrapes advertisments from groups and scores them with chatgpt
    def __get_group_advertisments_score(
        self, limit: int, group: str, preferences: Preferences
    ) -> List[dict]:
        # get posts generator from scraper
        advertisments = self.scraper.get_posts(group=group)
        # yield chatgpt generated posts until limit
        for i, advertisment in zip(range(limit), advertisments):
            # next advertisment's score from chatgpt
            advertisment = self.chatGPT.score_advertisment(
                advertisment=advertisment, preferences=preferences
            )
            # continue if its a searcher post as it is not relevant for us
            if advertisment["searcher_post"]:
                continue
            # yield advertisment
            yield advertisment

    # public for returning advertisments
    def get_advertisments(self, user_id: int, limit: int) -> List[dict]:
        # get user preferences
        preferences = self.__get_preferences(user_id)
        # get user groups
        groups = self.__get_groups(user_id)
        return [
            adv
            for adv in self.__get_group_advertisments_score(
                limit=limit, group=groups[0], preferences=preferences
            )
        ]
