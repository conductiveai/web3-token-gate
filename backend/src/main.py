import logging
from typing import Union, Type, Callable, Any

from fastapi import FastAPI
from flask import Response
from starlette.middleware.cors import CORSMiddleware
from starlette.testclient import TestClient

from settings import settings
from routes import organization, context, contract
from routes import user
from routes import superadmin
from routes import verification
from routes import exception


def create_app() -> FastAPI:

    # Configuring logging
    logging.basicConfig(level=settings.log_level, format=settings.log_format)

    # Instantiate app
    app: FastAPI = FastAPI(
        title=settings.title, version=settings.version, debug=settings.debug
    )

    # Add CORS support
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=".*",
        allow_methods=("GET", "POST", "PUT", "DELETE", "OPTIONS"),
        allow_headers=("content-type", "authorization"),
    )

    @app.on_event("startup")
    async def startup_event():
        """ Create default chains """

        from models.chain import Chain

        for chain_id, name in settings.chains.items():
            Chain.get_or_create(
                id=chain_id,
                defaults={
                    'name': name
                }
            )

    # Add routers
    app.include_router(organization.router, prefix="/organization")
    app.include_router(user.router, prefix="/user")
    app.include_router(verification.router, prefix="/verification")
    app.include_router(superadmin.router, prefix="/superadmin")
    app.include_router(contract.router, prefix="/process_contracts")
    app.include_router(context.router, prefix="/context")

    # Add exceptions handling
    exception_cls: Union[int, Type[Exception]]
    exception_handler: Callable[..., Any]

    # Add all the exception handlers to the app instance
    for exception_cls, exception_handler in exception.exception_router.items():
        app.add_exception_handler(exception_cls, exception_handler)

    return app


def entrypoint(request):
    """ Entrypoint function for GCF. Uses FastAPI test client to dispatch flask requests """

    client = TestClient(create_app())
    response = client.request(method=request.method, url=request.url, headers=request.headers, content=request.data)
    return Response(response.content, status=response.status_code, headers=dict(response.headers))
