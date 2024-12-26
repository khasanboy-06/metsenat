
from celery import shared_task

@shared_task
def test():
    return "Task Completed!"
