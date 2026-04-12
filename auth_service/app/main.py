from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.security import HTTPBearer
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.api.router import api_router

security = HTTPBearer(auto_error=False)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(
    title="Auth Service",
    description="Сервис аутентификации",
    version="1.0.0",
    lifespan=lifespan,
    swagger_ui_parameters={
        "persistAuthorization": True,
        "displayRequestDuration": True
    }
)

app.include_router(api_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )
