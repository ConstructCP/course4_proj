from django.core.management.base import BaseCommand

from movies.omdb_integration import search_and_save


class Command(BaseCommand):
    help = 'Search OMDb and populate database with results'

    def add_arguments(self, parser):
        parser.add_argument('search', nargs='+')

    def handle(self, *args, **kwargs):
        search = ' '.join(kwargs['search'])
        search_and_save(search)
