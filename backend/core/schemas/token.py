from pydantic import BaseModel

class Token(BaseModel):
    AccessToken: str
    RefreshToken: str | None = None
    token_type: str = "Bearer"