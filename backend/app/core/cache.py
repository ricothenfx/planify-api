import json
import logging
from datetime import datetime
import redis.asyncio as aioredis
from app.core.config import settings

redis_client = aioredis.from_url(
    settings.REDIS_URL,
    encoding="utf-8",
    decode_responses=True,
)

logger = logging.getLogger(__name__)


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


class CacheService:
    def __init__(self, prefix: str = "planify", ttl: int = 300):
        self.prefix = prefix
        self.ttl = ttl

    def _key(self, key: str) -> str:
        return f"{self.prefix}:{key}"

    async def get(self, key: str) -> dict | list | None:
        try:
            data = await redis_client.get(self._key(key))
            if data:
                logger.debug(f"🟢 CACHE HIT: {self._key(key)}")
                return json.loads(data)
            logger.debug(f"🔴 CACHE MISS: {self._key(key)}")
            return None
        except Exception:
            return None

    async def set(self, key: str, value: dict | list, ttl: int | None = None) -> None:
        try:
            await redis_client.setex(
                self._key(key),
                ttl or self.ttl,
                json.dumps(value, cls=DateTimeEncoder),
            )
            logger.debug(f"✅ CACHE SET: {self._key(key)}")
        except Exception as e:
            logger.error(f"❌ CACHE SET ERROR: {self._key(key)} - {e}")

    async def delete(self, key: str) -> None:
        try:
            await redis_client.delete(self._key(key))
        except Exception:
            pass

    async def delete_pattern(self, pattern: str) -> None:
        try:
            keys = await redis_client.keys(f"{self.prefix}:{pattern}")
            if keys:
                await redis_client.delete(*keys)
        except Exception:
            pass