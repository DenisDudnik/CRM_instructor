from settings import env

broker_transport_options = {'visibility_timeout': 3600}
result_backend = env("CELERY_BROKER_URL", default="redis://redis:6379/0")
task_track_started = True
task_serializer = 'pickle'
result_serializer = 'pickle'
accept_content = ['application/json', 'application/x-python-serialize', 'pickle']

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#beat-scheduler
beat_scheduler = "django_celery_beat.schedulers:DatabaseScheduler"

CELERY_TASK_ROUTES = {
    # указать путь до функции выполняющейся в Celery
    # 'apps.logistic_x.tasks.save_report': {'queue': 'quick', 'routing_key': 'quick'},
}
