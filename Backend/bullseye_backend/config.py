import os
from dotenv import load_dotenv
from starlette.config import Config
from authlib.integrations.starlette_client import OAuth
import secrets

load_dotenv(".env")


class OauthSettings:
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID") or None
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET") or None


class Settings:
    PROJECT_NAME: str = "Bullseye"
    PROJECT_VERSION: str = "1.0.0"

    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv(
        "POSTGRES_PORT", 5432
    )  # default postgres port is 5432
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "tdd")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:5432/{POSTGRES_DB}"


OauthSettings = OauthSettings()
settings = Settings()

SECRET_KEY = os.getenv("SECRET_KEY") or None


def isConfigured():
    if (
        OauthSettings.GOOGLE_CLIENT_ID is None
        or OauthSettings.GOOGLE_CLIENT_SECRET is None
    ):
        raise BaseException("Missing env variable")
    if SECRET_KEY is None:
        raise "Missing SECRET_KEY"
    return True


def OathSetUp():
    config_data = {
        "GOOGLE_CLIENT_ID": OauthSettings.GOOGLE_CLIENT_ID,
        "GOOGLE_CLIENT_SECRET": OauthSettings.GOOGLE_CLIENT_SECRET,
    }
    starlette_config = Config(environ=config_data)
    oauth = OAuth(starlette_config)
    oauth.register(
        name="google",
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )
    return oauth
