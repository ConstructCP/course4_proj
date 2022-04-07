import logging
import re
from datetime import timedelta

from django.utils.timezone import now

from movies.models import Genre, Movie, SearchTerm
from omdb.django_client import get_client_from_settings

logger = logging.getLogger(__name__)


def get_or_create_genres(genre_names):
    for genre_name in genre_names:
        genre, is_created = Genre.objects.get_or_create(name=genre_name)
        yield genre


def fill_movie_details(movie):
    if movie.is_full_record:
        logger.warning('"%s" is already a full record', movie.title)
        return

    omdb_client = get_client_from_settings()
    movie_details = omdb_client.get_by_imdb_id(movie.imdb_id)
    movie.year = movie_details.year
    movie.plot = movie_details.plot
    movie.runtime_minutes = movie_details.runtime_minutes
    movie.genres.clear()
    for genre in get_or_create_genres(movie_details.genres):
        movie.genres.add(genre)
    movie.is_full_record = True
    movie.save()


def search_and_save(search):
    normalized_search_term = re.sub(r'\s+', ' ', search.lower())
    search_term, is_created = SearchTerm.objects.get_or_create(term=normalized_search_term)
    was_searched_less_than_24h_ago = search_term.last_search > now() - timedelta(days=1)
    if not is_created and was_searched_less_than_24h_ago:
        logger.warning('Search for "%s" was performed less than 24h ago.', normalized_search_term)
        return

    omdb_client = get_client_from_settings()
    
    for omdb_movie in omdb_client.search(search):
        logging.info('Saving movie: "%s" / "%s"', omdb_movie.title, omdb_movie.imdb_id)
        movie, is_created = Movie.objects.get_or_create(
            imdb_id=omdb_movie.imdb_id,
            defaults={
                'title': omdb_movie.title,
                'year': omdb_movie.year,
            }
        )

        if is_created:
            logger.info('Movie created: "%s"', movie.title)

    search_term.save()
