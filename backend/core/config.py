from typing import Any, Dict, List, Optional, Union
from pydantic_settings import BaseSettings
from pydantic import BaseModel
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class DBSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    echo: bool = False

    class Config:
        env_file = BASE_DIR.parent / ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    @property
    def url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:"
            f"{self.DB_PASSWORD}@{self.DB_HOST}:"
            f"{self.DB_PORT}/{self.DB_NAME}"
        )

class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "Certs"/ "private.pem"
    public_key_path: Path = BASE_DIR / "Certs" / "public.pem"
    algorithm: str = "RSA256"

class Settings(BaseModel):
    db: DBSettings =  DBSettings()
    img_path: Path = BASE_DIR / "static" / "img"
    deffault_avatar_img : Path = img_path / "user.png"
    auth_jwt: AuthJWT = AuthJWT()
    pass

settings = Settings()