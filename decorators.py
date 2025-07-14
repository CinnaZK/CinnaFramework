import asyncio
import logging
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable, TypeVar
import hashlib
import json

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=Callable)


def with_cache(ttl_seconds: int = 300):
    """
    Decorator to cache async method results per class, with TTL.
    Features:
        - Shared cache across all instances of the same class
        - Thread-safe using Python dict atomicity
        - Avoids caching known error responses
    """
    def decorator(func: T) -> T:
        cache_key_base = f"_cache_{func.__name__}"
        ttl_key = f"_cache_ttl_{func.__name__}"
        hits_key = f"_cache_hits_{func.__name__}"
        misses_key = f"_cache_misses_{func.__name__}"

        @wraps(func)
        async def wrapper(self, *args, **kwargs) -> Any:
            # Initialize caches at class level
            cls = self.__class__
            for key in [cache_key_base, ttl_key, hits_key, misses_key]:
                if not hasattr(cls, key):
                    setattr(cls, key, {} if "cache" in key else 0)

            cache = getattr(cls, cache_key_base)
            cache_ttl = getattr(cls, ttl_key)

            try:
                args_str = json.dumps(args, sort_keys=True, default=str)
                kwargs_str = json.dumps(sorted(kwargs.items()), default=str)
                key_material = f"{func.__name__}:{args_str}:{kwargs_str}"
                cache_key = hashlib.md5(key_material.encode()).hexdigest()
            except (TypeError, ValueError):
                cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
                logger.warning(f"Fallback cache key used for {func.__name__}")

            logger.debug(f"Cache key for {func.__name__}: {cache_key}")

            if cache_key in cache and datetime.now() < cache_ttl[cache_key]:
                setattr(cls, hits_key, getattr(cls, hits_key) + 1)
                logger.debug(f"Cache hit for {func.__name__}")
                return cache[cache_key]

            setattr(cls, misses_key, getattr(cls, misses_key) + 1)
            logger.debug(f"Cache miss for {func.__name__}")

            result = await func(self, *args, **kwargs)

            # Avoid caching known error patterns
            should_cache = True
            if isinstance(result, dict) and ("error" in result or result.get("status") == "error"):
                should_cache = False
                logger.debug(f"Skipping cache for error response from {func.__name__}")

            if should_cache:
                cache[cache_key] = result
                cache_ttl[cache_key] = datetime.now() + timedelta(seconds=ttl_seconds)

            if len(cache) > 10000:
                oldest_keys = sorted(cache_ttl.items(), key=lambda x: x[1])[:len(cache) - 100]
                for k, _ in oldest_keys:
                    cache.pop(k, None)
                    cache_ttl.pop(k, None)

            return result

        return wrapper

    return decorator


def with_retry(max_retries: int = 3, delay: float = 1.0):
    """
    Decorator for retrying async functions with exponential backoff.
    """
    def decorator(func: T) -> T:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            last_error = None
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < max_retries - 1:
                        delay_time = delay * (2 ** attempt)
                        logger.warning(f"Retry {attempt + 1}/{max_retries} for {func.__name__} after {delay_time}s")
                        await asyncio.sleep(delay_time)

            logger.error(f"All retries failed for {func.__name__}: {last_error}")
            raise last_error

        return wrapper

    return decorator


def monitor_execution():
    """
    Decorator to log async function execution time and success/failure.
    """
    def decorator(func: T) -> T:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            start_time = datetime.now()
            try:
                result = await func(*args, **kwargs)
                elapsed = (datetime.now() - start_time).total_seconds()
                logger.info(f"{func.__name__} executed successfully in {elapsed:.2f}s")
                return result
            except Exception as e:
                elapsed = (datetime.now() - start_time).total_seconds()
                logger.error(f"{func.__name__} failed after {elapsed:.2f}s: {e}")
                raise

        return wrapper

    return decorator
