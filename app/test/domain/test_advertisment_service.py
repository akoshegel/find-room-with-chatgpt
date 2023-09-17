import logging
from app.dependencies import Dependencies

logger = logging.getLogger(name="test_advertisment_service")
advertisment_service = Dependencies.make_advertisment_service()


def test_get_advertisments():
    advertisments = advertisment_service.get_advertisments(1, 1)
    logger.info(advertisments)
