import redis
from backend.src.config.settings import settings

redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

def store_token(user_id: str, token: str, ttl: int) -> None:
    redis_client.setex(f"user:{user_id}:token", ttl, token)

def get_token(user_id: str) -> str | None:
    return redis_client.get(f"user:{user_id}:token")

def delete_token(user_id: str) -> None:
    redis_client.delete(f"user:{user_id}:token")

class RedisClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RedisClient, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, host='localhost', port=6379, db=0):
        if self._initialized:
            return
        import redis
        self.client = redis.StrictRedis(host=host, port=port, db=db)
        self._initialized = True

    def get_client(self):
        return self.client
