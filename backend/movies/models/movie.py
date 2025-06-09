from django.db import models
from movies.managers.movie_manager import MovieManager

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "genre"

    def __str__(self):
        return self.name


class ProductionCompany(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "production_company"

    def __str__(self):
        return self.name


class ProductionCountry(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "production_country"

    def __str__(self):
        return self.name


class SpokenLanguage(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "spoken_language"

    def __str__(self):
        return self.name


class Keyword(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "keyword"

    def __str__(self):
        return self.name


class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255, db_index=True)
    original_title = models.CharField(max_length=255)
    vote_average = models.FloatField(db_index=True)
    vote_count = models.IntegerField()
    status = models.CharField(max_length=50)
    release_date = models.DateField(null=True, blank=True, db_index=True)
    revenue = models.BigIntegerField()
    runtime = models.IntegerField()
    adult = models.BooleanField(db_index=True)
    backdrop_path = models.CharField(max_length=255, null=True, blank=True)
    poster_path = models.CharField(max_length=255, null=True, blank=True)
    budget = models.BigIntegerField()
    homepage = models.URLField(null=True, blank=True)
    imdb_id = models.CharField(max_length=20, null=True, blank=True)
    original_language = models.CharField(max_length=10)
    overview = models.TextField(null=True, blank=True)
    popularity = models.FloatField(db_index=True)
    tagline = models.TextField(null=True, blank=True)

    genres = models.ManyToManyField(Genre)
    production_companies = models.ManyToManyField(ProductionCompany)
    production_countries = models.ManyToManyField(ProductionCountry)
    spoken_languages = models.ManyToManyField(SpokenLanguage)
    keywords = models.ManyToManyField(Keyword)

    objects = MovieManager()

    class Meta:
        db_table = "movie"
        indexes = [
            models.Index(fields=["title", "adult"]),
        ]

    def __str__(self):
        return self.title

    @property
    def poster_url(self):
        if self.poster_path:
            return f"https://image.tmdb.org/t/p/w342{self.poster_path}"
        return None

    @property
    def backdrop_url(self):
        if self.backdrop_path:
            return f"https://image.tmdb.org/t/p/w780{self.backdrop_path}"
        return None