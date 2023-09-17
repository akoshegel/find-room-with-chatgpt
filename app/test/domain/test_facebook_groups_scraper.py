import logging
from app.dependencies import Dependencies


logger = logging.getLogger("test_chatgpt_logger")


def test_make_chatgpt_service():
    scraper = Dependencies.make_scraper()
    post = next(scraper.get_posts("914912568563514"))
    assert type(post["link"]) is str
    assert type(post["text"]) is str
    assert type(post["timestamp"]) is int
