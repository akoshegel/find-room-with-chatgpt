import logging
from app.dependencies import Dependencies


logger = logging.getLogger("test_chatgpt_logger")


def test_make_chatgpt_service():
    chatgpt = Dependencies.make_chatgpt()
    response = chatgpt.rate_advertisment(
        {
            "text": "We offer a large room. No couples. Natural light and big couch.",
            "link": "link_to_post",
            "timestamp": 1234,
        },
        [[3, "Move with my partner"]],
    )
    assert type(response) is dict
    assert response["timestamp"] == 1234
    assert (
        response["text"]
        == "We offer a large room. No couples. Natural light and big couch."
    )
    assert response["link"] == "link_to_post"
    assert type(response["score"]) is int
    assert type(response["reasoning"]) is str
    assert type(response["searcher_post"]) is bool
