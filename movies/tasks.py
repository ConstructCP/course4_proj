from django.core.mail import mail_admins
from django.utils import timezone
from celery import shared_task

from movies import omdb_integration
from movies.Models import MovieNight


@shared_task
def search_and_save(search):
    return omdb_integration.search_and_save(search)


@shared_task
def notify_of_new_search_term(search_term):
    mail_admins('New Search Term', f'A new search term was used: "{search_term}"')


@shared_task
def get_today_search_terms_number():
    search_number = SearchTerm.objects.filter(
        start__gte=timezone.now().replace(hour=0, minute=0, second=0), 
        end__lte=timezone.now().replace(hour=23, minute=59, second=59)
    ).count()
    print(f'Today search number: {search_number}')

