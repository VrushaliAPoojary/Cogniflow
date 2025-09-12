from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@postgres:5432/assignmentdb"
    OPENAI_API_KEY: str = ""
    CHROMA_PERSIST_DIR: str = "/data/chroma"
    SERPAPI_KEY: str = ""
    # server host/port
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"

settings = Settings()
