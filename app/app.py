from fastapi import FastAPI
from app.dependencies import Dependencies
from app.config import Config

# getting config
config = Config.get()

# advertisment service to retieve ads
advertisment_service = Dependencies.make_advertisment_service()

# fastapi application
app = FastAPI()


# route for retrieving scored advertisment for user
@app.get("/")
def read_advertisments(limit: int = 5, user_id: int = 1):
    # returning data from advertisment service
    return advertisment_service.get_advertisments(user_id=1, limit=5)
