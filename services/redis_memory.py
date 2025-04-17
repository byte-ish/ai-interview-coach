import json
import logging
import redis
import uuid
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()
logger = logging.getLogger(__name__)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

class RedisSessionStore:
    def __init__(self):
        try:
            self.redis = redis.Redis.from_url(REDIS_URL, decode_responses=True)
            self.redis.ping()
            logger.info("Connected to Redis successfully.")
        except redis.RedisError as e:
            logger.exception("Failed to connect to Redis.")
            raise

    def save_session(self, session_data: dict, session_id: Optional[str] = None) -> str:
        try:
            if not session_id:
                session_id = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + str(uuid.uuid4())[:8]
            key = f"session:{session_id}"
            self.redis.set(key, json.dumps(session_data))
            logger.info(f"Session saved to Redis with ID: {session_id}")
            return session_id
        except Exception as e:
            logger.exception("Failed to save session to Redis.")
            raise

    def load_session(self, session_id: str) -> dict:
        try:
            key = f"session:{session_id}"
            data = self.redis.get(key)
            if not data:
                raise ValueError(f"Session ID {session_id} not found in Redis.")
            return json.loads(data)
        except Exception as e:
            logger.exception(f"Failed to load session ID {session_id} from Redis.")
            raise

    def list_sessions(self) -> list:
        try:
            keys = self.redis.keys("session:*")
            return [key.split(":", 1)[1] for key in keys]
        except Exception as e:
            logger.exception("Failed to list sessions from Redis.")
            raise