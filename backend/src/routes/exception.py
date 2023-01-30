from typing import Dict

from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from exceptions.exceptions import ApiError
from schemas.error import ApiError as ApiErrorSchema


async def api_exception_handler(
    request: Request,
    exc: ApiError
) -> JSONResponse:
    error = ApiErrorSchema(message=exc.message)

    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=error.dict())


async def internal_exception_handler(request: Request, exc: Exception) -> JSONResponse:

    error_message: str = "Internal server error."
    error = ApiErrorSchema(message=error_message)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error.dict()
    )


exception_router: Dict = {
    ApiError: api_exception_handler,
    Exception: internal_exception_handler,
}
