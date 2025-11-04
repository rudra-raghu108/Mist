# app/api/v1/api.py
from fastapi import APIRouter

# Optional SlowAPI
SLOWAPI_AVAILABLE = True
try:
    from slowapi import Limiter
    from slowapi.util import get_remote_address
except Exception:
    SLOWAPI_AVAILABLE = False
    Limiter = None
    get_remote_address = None

router = APIRouter()

# If SlowAPI is present, create a limiter; else, use a no-op decorator
if SLOWAPI_AVAILABLE:
    limiter = Limiter(key_func=get_remote_address)
    def rate_limit(rule: str):
        return limiter.limit(rule)
else:
    def rate_limit(rule: str):  # no-op decorator
        def wrapper(func):
            return func
        return wrapper

@router.get("/ping", tags=["Utility"])
@rate_limit("10/minute")
async def ping():
    return {"message": "pong"}
