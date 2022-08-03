from celery import app as celery_app
from .utils import notify_all_subscribers, notify_post_create
from celery.schedules import crontab


@celery_app.task
def notify_post_create_celery(
        sender, instance, action, **kwargs
):
    notify_post_create(
        sender=sender,
        instance=instance,
        action=action,
        **kwargs,
    )


@celery_app.task
def notify_all_subscribers_celery():
    notify_all_subscribers()


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=8, minute=0, day_of_week=1),
        notify_post_create_celery.s(),
    )
