import os
from fastapi_mail import ConnectionConfig
from jinja2 import Environment, select_autoescape, PackageLoader


google_credentials = {
    "web": {
        "client_id": "1059122565838-ssslohu20habg3ie5g66ov750jo7dq0p.apps.googleusercontent.com",
        "project_id": "jiraclone-378110",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "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",
        "redirect_uris": [
            "http://127.0.0.1:8008/",
            "http://127.0.0.1:8008/login/google/callback",
        ],
        "javascript_origins": ["http://127.0.0.1:8008"],
    }
}

email_configuration = ConnectionConfig(
    MAIL_USERNAME="simbasingh1999@gmail.com",
    MAIL_PASSWORD="qwjiusbmxhdjpozb",
    MAIL_FROM="simbasingh1999@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="Shibham singh",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


# first parameter is app name
# here in package loader second parameter is path of tempalte folder if we don't provide it will take templates
template_env = Environment(
    loader=PackageLoader("app"), autoescape=select_autoescape(["html", "xml"])
)


class Settings:
    PROJECT_NAME: str = "Jira Clone lx"
    PROJECT_VERSION: str = "1.0.0"

    POSTGRES_USER: str = os.getenv("DB_USERNAME")
    POSTGRES_PASSWORD = os.getenv("DB_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("DB_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("DB_PORT", 5432)
    POSTGRES_DB: str = os.getenv("DB_NAME")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"


settings = Settings()
