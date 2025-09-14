from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/assignmentdb"
    OPENAI_API_KEY: str = ""
    CHROMA_PERSIST_DIR: str = "./chroma_data"
    SERPAPI_KEY: str = ""

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"

settings = Settings()
