from fastapi import Response

class SetTokenCookie():
    def __init__(self,
                 token: str | None,
                 key: str = 'refresh_token',
                 httponly: bool = True,
                 secure: bool = True,
                 samesite: str = 'lax',
                 max_age: int = 60*60*24*7
                 ):
        self.value = token,
        self.key = key,
        self.httponly = httponly,
        self.secure = secure,
        self.samesite = samesite,
        self.max_age = max_age

    def update_response(self, response: Response):
        return response.set_cookie(
            key= self.key,
            value= self.value,
            max_age= self.max_age,
            secure= self.secure,
            samesite= self.samesite,
            httponly=self.httponly
        )

    def delete_cookie_from_response(self, response: Response):
        return response.delete_cookie(key=self.key)