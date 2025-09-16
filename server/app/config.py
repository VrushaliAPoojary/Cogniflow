from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/assignment_db"
    OPENAI_API_KEY: str = ""
    CHROMA_PERSIST_DIR: str = "./chroma_data"
    SERPAPI_KEY: str = ""

    # LLM settings
    USE_LOCAL_LLM: bool = False
    LOCAL_LLM_MODEL: str = "tiiuae/mistral-7b-instruct"

    # Embeddings
    USE_LOCAL_EMBEDDINGS: bool = False
    LOCAL_EMBED_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
