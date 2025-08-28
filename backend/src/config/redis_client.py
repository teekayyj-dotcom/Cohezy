import redis
from backend.src.config.settings import settings
from backend.src.core.logger import get_logger

logger = get_logger(__name__)

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    password=settings.REDIS_PASSWORD,
    decode_responses=True
)

def init_redis():
    try:
        redis_client.ping()
        logger.info("Connected to Redis successfully.")
    except redis.ConnectionError as e:
        logger.error(f"Failed to connect to Redis: {e}")
        raise

def close_redis():
    try:
        redis_client.close()
        logger.info("Disconnected from Redis successfully.")
    except Exception as e:
        logger.error(f"Failed to disconnect from Redis: {e}")
        raise

