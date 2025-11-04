# app/core/celery.py
from celery import Celery
from app.core.config import settings

celery_app: Celery | None = None

def init_celery():
    global celery_app
    if celery_app is None:
        celery_app = Celery(
            "srm_guide_bot",
            broker=settings.REDIS_URL,
            backend=settings.REDIS_URL,
            include=[],
        )
        # Optional config
        celery_app.conf.update(
            task_serializer="json",
            accept_content=["json"],
            result_serializer="json",
            timezone="UTC",
            worker_max_tasks_per_child=100,
        )
