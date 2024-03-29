from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.auth.base_config import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate
from fastapi.middleware.cors import CORSMiddleware
from src.config import REDIS_HOST, REDIS_PORT
from src.operations.router import router as router_operation
from src.tasks.router import router as router_send_email
from src.pages.router import router as router_pages
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import aioredis


app = FastAPI(
    title="Trading App"
)


# подключение статики
app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_operation)
app.include_router(router_send_email)
app.include_router(router_pages)


origins = [
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT', 'DELETE'],
    allow_headers=['Content-Type', 'Set-Cookie', 'Access-Control-Allow-Headers', 'Access-Control-Allow-Origin',
                   'Authorization'],
)


# для использования декоратора "cache"
@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding="utf8", decode_response=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
