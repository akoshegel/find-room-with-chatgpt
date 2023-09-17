import logging
from typing import TypedDict, List

import facebook_scraper

# logger for facebook_groups file
logger = logging.getLogger(name="facebook_groups")


# type for FacebookPost
class FacebookPost(TypedDict):
    text: str
    link: str
    timestamp: int


# type for FacebookGroupsScraperConfig
class FacebookGroupsScraperConfig(TypedDict):
    pages: int
    posts_per_pages: int
    timeout: int


# facebook scraper service, gets scraper as dependency
class FacebookGroupsScraper:
    def __init__(
        self,
        scraper: facebook_scraper,
        config: FacebookGroupsScraperConfig = {
            "timeout": 30,
            "pages": 2,
            "posts_per_pages": 1,
        },
    ):
        self.scraper = scraper
        # setting config for scraper
        self.config = config

    # used to get posts from facebook group
    def __get_posts(self, group: str):
        # get posts from group page
        return self.scraper.get_posts(
            group,
            timeout=self.config["timeout"],
            pages=self.config["pages"],
            extra_info=False,
            youtube_dl=False,
            options={
                "posts_per_pages": self.config["posts_per_pages"],
                "comments": False,
                "reactors": False,
                "progress": False,
            },
        )

    # yield transformed posts one by one
    def get_posts(self, group: str) -> List[FacebookPost]:
        for post in self.__get_posts(group):
            if not post["text"] or not post["post_url"] or not post["timestamp"]:
                continue
            yield {
                "text": post["text"],
                "link": post["post_url"],
                "timestamp": int(post["timestamp"]),
            }
