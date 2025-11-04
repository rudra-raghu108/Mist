"""
Redis configuration for SRM Guide Bot (Local Dev Mode)
Temporarily disables Redis to allow backend to start without it.
"""

import logging
logger = logging.getLogger(__name__)

# Redis client placeholder
redis_client = None


async def init_redis():
    """Skip Redis initialization during local testing"""
    try:
        logger.warning("⚠️ Redis temporarily disabled for local testing.")
        return None
    except Exception as e:
        logger.warning(f"Skipping Redis initialization due to: {e}")
        return None


async def close_redis():
    """Skip closing Redis"""
    logger.info("⚠️ Redis close skipped (disabled for local testing).")


async def get_redis_client():
    """Return None instead of Redis client"""
    logger.warning("⚠️ Redis client unavailable (disabled for local testing).")
    return None


async def set_cache(key: str, value: str, expire: int = None):
    """Skip caching"""
    logger.debug(f"Redis disabled: Skipping set_cache for key={key}")


async def get_cache(key: str) -> str:
    """Skip fetching cache"""
    logger.debug(f"Redis disabled: Skipping get_cache for key={key}")
    return None


async def delete_cache(key: str):
    """Skip deleting cache"""
    logger.debug(f"Redis disabled: Skipping delete_cache for key={key}")


async def clear_cache():
    """Skip clearing cache"""
    logger.debug("Redis disabled: Skipping clear_cache()")
