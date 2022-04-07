from django.conf import settings

from omdb.client import OmdbClient


def get_client_from_settings():
    return OmdbClient(settings.OMDB_KEY)
