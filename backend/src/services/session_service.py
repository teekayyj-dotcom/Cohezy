import uuid
from datetime import datetime, timedelta
from backend.src.config.redis_client import redis_client
from backend.src.config.settings import settings

class SessionService:
    @staticmethod
    def create_session(session_id: str, user_id: str) -> str:
        session_token = str(uuid.uuid4())
        expires_at = datetime.utcnow() + timedelta(seconds=settings.SESSION_TOKEN_TTL)
        redis_key = f"session:{session_id}:token"
        redis_client.setex(redis_key, settings.SESSION_TOKEN_TTL, session_token)
        return session_token
    
    @staticmethod
    def verify_session(session_id: str, session_token: str) -> bool:
        redis_key = f"session:{session_id}:token"
        stored_token = redis_client.get(redis_key)
        return stored_token == session_token
    
    @staticmethod
    def revoke_session_token(session_id: str, user_id: str) -> None:
        redis_key = f"session:{session_id}:token"
        redis_client.delete(redis_key)