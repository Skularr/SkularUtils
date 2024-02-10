from os import getenv

from httpx import AsyncClient, URL


class Google:
    google_auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
    scope = "openid email profile"
    response_type = "code"
    redirect_base_url = getenv("REDIRECT_BASE_URL")
    client_id = getenv("CLIENT_ID")
    client_secret = getenv("CLIENT_SECRET")
    token_url = "https://oauth2.googleapis.com/token"
    userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"

    @classmethod
    async def get_url(cls, state, redirect: str) -> URL:
        query = {
            "client_id": cls.client_id,
            "redirect_uri": f'{cls.redirect_base_url}/{redirect}',
            "scope": cls.scope,
            "response_type": cls.response_type,
            "state": state
        }
        url = URL(cls.google_auth_url, params=query)
        return url

    @classmethod
    async def get_token(cls, code: str, redirect: str) -> dict:
        token_request_data = {
            "code": code,
            "client_id": cls.client_id,
            "client_secret": cls.client_secret,
            "redirect_uri": f'{cls.redirect_base_url}/{redirect}',
            "grant_type": "authorization_code"
        }
        client = AsyncClient()
        response = await client.post(cls.token_url, data=token_request_data)
        token_data = response.json()
        return token_data

    @classmethod
    async def get_userinfo(cls, access_token: str) -> dict | None:
        query = {
            "access_token": access_token
        }
        client = AsyncClient()
        response = await client.get(cls.userinfo_url, params=query)
        if response.status_code == 200:
            userinfo = response.json()
            return userinfo
        return None
