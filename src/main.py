from fastapi import FastAPI
from src.auth.base_config import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate
from src.config import REDIS_HOST, REDIS_PORT
from src.operations.router import router as router_operation
from src.tasks.router import router as router_send_email
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import aioredis




app = FastAPI(
    title="Trading App"
)

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


# после этого можем пользоваться декоратором cache для кэширования ответов.
@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding="utf8", decode_response=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
