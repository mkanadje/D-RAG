from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache
import os
from app import ROOT_PATH


# Settings (child of BaseSettings) reads environment settings in the following order:
# 1. Environment variables
# 2. .env_file
# 3. Default values defined in the class
class Settings(BaseSettings):
    OPENAI_API_KEY: str
    MODEL_NAME: str = "gpt-4o-mini"

    DATA_FOLDER_PATH: str = os.path.join(ROOT_PATH, "..", "rag", "data")
    VECTOR_DB_PATH: str = os.path.join(ROOT_PATH, "..", "rag", "vector_db")

    BACKEND_HOST: str = "http://localhost"
    BACKEND_PORT: str = "8501"
    # Model settings
    TEMPERATURE: float = 0.7

    MAX_TOKENS_PER_REQUEST: int = 250000
    MAX_CHUNK_SIZE_TOKENS: int = 1000
    CHUNK_OVERLAP_TOKENS: int = 200

    CHUNK_SIZE: int = MAX_CHUNK_SIZE_TOKENS
    CHUNK_OVERLAP: int = CHUNK_OVERLAP_TOKENS

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        os.environ["OPENAI_API_KEY"] = self.OPENAI_API_KEY

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Function decoration to cache the settings instance. It avoids re-reading the .env
# file on every call.
@lru_cache()
def get_settings() -> Settings:
    return Settings()
