import redis
from ..config.settings import settings

class RedisService:
    client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True)

@staticmethod
def set_token(user_id: str, token: str, expires_in: int) -> None:
    RedisService.client.setex(user_id, expires_in, token)

@staticmethod
def get_token(user_id: str) -> str | None:
    return RedisService.client.get(user_id)

@staticmethod
def delete_token(user_id: str) -> None:
    RedisService.client.delete(user_id)