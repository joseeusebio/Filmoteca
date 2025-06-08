from django.db import models

class MovieManager(models.Manager):
    def public(self):
        return self.get_queryset().filter(adult=False).order_by(
            '-release_date',
            '-popularity',
            'title'
        ).prefetch_related(
            'genres', 'production_companies', 'production_countries',
            'spoken_languages', 'keywords'
        )
