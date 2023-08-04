import os
from pydantic import BaseSettings

class Settings(BaseSettings):

    ANNOQ_ES_URL:str = os.environ.get("ANNOQ_ES_URL")
    ANNOQ_ANNOTATIONS_INDEX :str = os.environ.get("ANNOQ_ANNOTATIONS_INDEX")
    ANNOQ_TERMS_INDEX:str = os.environ.get("ANNOQ_TERMS_INDEX")
    PROJECT_VERSION: str = "0.0.1"
    HOST_HTTP: str = os.environ.get("HOST_HTTP","http://")
    HOST_URL: str = os.environ.get("HOST_URL")
    HOST_PORT: int = int(os.environ.get("HOST_PORT"))
    BASE_URL: str = HOST_HTTP+HOST_URL+":"+str(HOST_PORT)


settings = Settings()