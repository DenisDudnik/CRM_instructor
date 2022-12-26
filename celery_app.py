# quick_publisher/celery.py

import os

from celery import Celery
from celery.schedules import crontab
from celery.signals import setup_logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

app = Celery('users')
app.config_from_object('settings.celery', namespace="CELERY")


@setup_logging.connect
def config_loggers(*args, **kwags):
    from logging.config import dictConfig

    from django.conf import settings
    dictConfig(settings.LOGGING)


# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'Lesson_notifications': {
        'task': 'users.tasks.lesson_notifications',
        'schedule': crontab(minute=1, hour=0)
        # 'schedule': 30.0
    }
    # 'task_export_routes': {
    #     'task': 'apps.verification.tasks.task_export_routes',
    #     'schedule': crontab(),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
    #     'options': {'queue': 'quick'}
    # },
    # 'task_export_combination': {
    #     'task': 'apps.verification.tasks.task_export_combination',
    #     'schedule': crontab(),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
    #     'options': {'queue': 'quick'}
    # },
    # 'get_params': {
    #     'task': 'apps.verification.tasks.task_get_admin_params',
    #     'schedule': crontab(),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
    #     'options': {'queue': 'quick'}
    # },
    # 'update_status': {
    #     'task': 'apps.logistic_x.tasks.task_update_status',
    #     'schedule': 15.0,  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
    #     'options': {'queue': 'quick'}
    # },
    # 'update_expired_status': {
    #     'task': 'apps.logistic_x.tasks.task_update_expired_status',
    #     'schedule': crontab(minute="*/2"),
    #     'options': {'queue': 'quick'}
    # },
    # 'task_set_last_job': {
    #     'task': 'apps.logistic_x.tasks.task_set_last_job',
    #     'schedule': 15.0,  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
    #     'options': {'queue': 'quick'}
    # },
    # "archive_action_entries": {
    #     "task": "apps.logactions.tasks.archive_action_entries",
    #     "schedule": crontab(minute=0, hour=0, day_of_week="sunday"),
    #     # "schedule": crontab(minute="*/1")     # for testing
    #     'options': {'queue': 'quick'}
    # },
    # "clear_action_logs": {
    #     "task": "apps.logactions.tasks.clear_action_logs",
    #     "schedule": crontab(minute=0, hour=0),
    #     # "schedule": crontab(minute="*/1")     # for testing
    #     'options': {'queue': 'quick'}
    # },
    # "execute_job_from_db": {
    #     "task": "apps.logistic_x.tasks.execute_job_from_db",
    #     "schedule": crontab(minute=0, hour=0),
    #     'options': {'queue': 'quick'},
    # },
}
