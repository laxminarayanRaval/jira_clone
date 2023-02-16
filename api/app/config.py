import os


class Settings:
    PROJECT_NAME: str = "Jira Clone lx"
    PROJECT_VERSION: str = "1.0.0"

    POSTGRES_USER: str = os.getenv("DB_USER")
    POSTGRES_PASSWORD = os.getenv("DB_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("DB_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("DB_PORT", 5432)
    POSTGRES_DB: str = os.getenv("DB_NAME")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"


settings = Settings()
