from celery import Celery

from app import config

celery_app = Celery(
    "app",
    broker=f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}/{config.REDIS_DB}",
    backend=f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}/{config.REDIS_DB}"
)

celery_app.conf.imports = [
    "app.orders.tasks",
]
