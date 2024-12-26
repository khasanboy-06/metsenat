import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.develop')
apps = Celery("core", broker=settings.CELERY_BROKER_URL)
apps.config_from_object("django.conf:settings", namespace="CELERY")

apps.autodiscover_tasks()

@apps.task
def test():
    return 0 

