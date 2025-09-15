from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./assignment.db"

    # LLM settings
    USE_LOCAL_LLM: bool = True
    LOCAL_LLM_MODEL: str = "distilgpt2"
    USE_LOCAL_EMBEDDINGS: bool = True
    LOCAL_EMBED_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    # OpenAI fallback
    OPENAI_API_KEY: str = ""

    # Vector DB
    CHROMA_PERSIST_DIR: str = "./chroma_data"

    class Config:
        env_file = "../.env"

settings = Settings()
