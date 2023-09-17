import logging
from os import getenv
from typing import TypedDict

from dotenv import load_dotenv

logger = logging.getLogger(name="config")
load_dotenv()


# defines the type of the config object
class ConfigObject(TypedDict):
    openai_api_key: str
    scraper_pages: int
    scraper_posts_per_pages: int
    scraper_timeout: int


# help manage config related operations
class Config:
    # gets config object
    @staticmethod
    def get():
        # define config object
        config_schema = {
            "openai_api_key": {"env": "OPENAI_API_KEY"},
            "scraper_pages": {"env": "SCRAPER_PAGES", "transform": lambda x: int(x)},
            "scraper_posts_per_pages": {
                "env": "SCRAPER_POSTS_PER_PAGES",
                "transform": lambda x: int(x),
            },
            "scraper_timeout": {
                "env": "SCRAPER_TIMEOUT",
                "transform": lambda x: int(x),
            },
        }
        config_object: ConfigObject = {}
        # validate config object
        for key, config in config_schema.items():
            # read env var value without default
            env_var = getenv(config["env"])
            # if env var is empty or env var type is wrong throw error
            if not env_var:
                raise Exception(f"missing env var: {env_var}")
            # transform and add value to config_object if it passed validation
            config_object[key] = (
                env_var if not config.get("transform") else config["transform"](env_var)
            )
        # returning config object
        return config_object
