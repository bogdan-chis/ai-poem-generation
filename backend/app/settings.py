from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MODEL_DIR: str = "../nichita-Ro-gpt2"
    DEVICE: str = "auto"          # "auto" | "cpu" | "cuda"
    ALLOW_CUDA: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
