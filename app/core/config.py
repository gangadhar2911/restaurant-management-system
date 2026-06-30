from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # DATABASE (built from individual parts in .env)
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "restaurant_management_system"
    DB_USER: str = "root"
    DB_PASSWORD: str = ""

    # SECURITY
    SECRET_KEY: str = "change_this_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # APP SETTINGS
    APP_NAME: str = "Restaurant Management System"
    DEBUG: bool = True

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()