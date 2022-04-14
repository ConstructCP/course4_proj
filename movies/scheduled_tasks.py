from django_celery_beat.models import IntervalSchedule
from django_celery_beat.models import PeriodicTask


def schedule_setup():
    """
    Should be run with something like:
    $ celery -A course4_proj beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
    """
    schedule, _ = IntervalSchedule.objects.get_or_create(every=1, period=IntervalSchedule.MINUTES)
    task = PeriodicTask.objects.create(
        interval=schedule,
        task='movies.tasks.get_today_search_terms_number',
        name='Print today search number to console'
    )
    task.save()
