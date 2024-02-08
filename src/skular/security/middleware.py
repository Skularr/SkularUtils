from loguru import logger
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from ..config.database import get_database
from .auth import get_token_data
from ..models.token import AccessTokenData


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, excluded_urls: list, **kwargs):

        self.excluded_urls = excluded_urls
        self.kwargs = kwargs
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        return await self.authentication_middleware(request, call_next)

    async def authentication_middleware(self, request: Request, call_next):
        full_path = request.url.path
        root_path: str = request.scope.get('root_path')
        mount_path = full_path.removeprefix(root_path)
        logger.debug(f"Full request path: {full_path}")
        logger.debug(f"Requested path in mount: {mount_path}")

        if mount_path in self.excluded_urls:
            logger.debug(f"Excluded path: {mount_path}")
            return await call_next(request)

        access_token = request.cookies.get("access_token")
        organization = request.cookies.get("organization")

        if not (access_token and organization):
            data = {"detail": "Please login to access"}
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=data)

        token_data: AccessTokenData
        success, token_data = await get_token_data(access_token, organization)
        if not success:
            data = {"detail": token_data}
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=data)

        user_id = token_data['sub']
        request.state.user = user_id
        request.state.token_data = token_data
        request.state.organization = organization
        request.state.access_token = access_token

        db_name = self.kwargs.get('db_name', organization)
        request.state.db = await get_database(db_name)

        response = await call_next(request)

        return response
