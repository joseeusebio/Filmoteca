import pandas as pd
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from tqdm import tqdm

from movies.models import (
    Movie, Genre, ProductionCompany, ProductionCountry, SpokenLanguage, Keyword
)


class Command(BaseCommand):
    help = 'Importa filmes com relacionamentos otimizados via bulk_create'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, required=True)
        parser.add_argument('--chunk', type=int, default=5000)
        parser.add_argument('--estimado', type=int, default=1000000)

    def handle(self, *args, **options):
        path = options['path']
        chunk_size = options['chunk']
        estimado = options['estimado']

        genre_cache = {g.name: g for g in Genre.objects.all()}
        company_cache = {c.name: c for c in ProductionCompany.objects.all()}
        country_cache = {c.name: c for c in ProductionCountry.objects.all()}
        language_cache = {l.name: l for l in SpokenLanguage.objects.all()}
        keyword_cache = {k.name: k for k in Keyword.objects.all()}

        novos_generos, novos_companies, novos_countries, novos_languages, novos_keywords = set(), set(), set(), set(), set()

        movie_genres = Movie.genres.through
        movie_companies = Movie.production_companies.through
        movie_countries = Movie.production_countries.through
        movie_languages = Movie.spoken_languages.through
        movie_keywords = Movie.keywords.through

        csv_iterator = pd.read_csv(path, chunksize=chunk_size)
        total_chunks = estimado // chunk_size

        for chunk in tqdm(csv_iterator, total=total_chunks, desc="Importando filmes"):
            movies = []
            filmes_com_row = []

            for _, row in chunk.iterrows():
                if pd.isna(row["id"]):
                    continue

                movie = Movie(
                    tmdb_id=row["id"],
                    title=row.get("title") or "",
                    original_title=row.get("original_title") or "",
                    vote_average=row.get("vote_average") or 0.0,
                    vote_count=row.get("vote_count") or 0,
                    status=row.get("status") or "",
                    release_date=self.parse_date(row.get("release_date")),
                    revenue=row.get("revenue") or 0,
                    runtime=row.get("runtime") or 0,
                    adult=str(row.get("adult")).lower() == 'true',
                    backdrop_path=row.get("backdrop_path"),
                    poster_path=row.get("poster_path"),
                    budget=row.get("budget") or 0,
                    homepage=row.get("homepage"),
                    imdb_id=row.get("imdb_id"),
                    original_language=row.get("original_language") or "",
                    overview=row.get("overview"),
                    popularity=row.get("popularity") or 0.0,
                    tagline=row.get("tagline")
                )
                movies.append(movie)
                filmes_com_row.append((movie, row))

            with transaction.atomic():
                Movie.objects.bulk_create(movies, batch_size=chunk_size, ignore_conflicts=True)

                tmdb_ids = [m.tmdb_id for m in movies]
                movie_map = {m.tmdb_id: m for m in Movie.objects.filter(tmdb_id__in=tmdb_ids)}

                for movie in movies:
                    movie.pk = movie_map[movie.tmdb_id].pk

                m2m_genres, m2m_companies, m2m_countries, m2m_languages, m2m_keywords = [], [], [], [], []
                reg_genres, reg_companies, reg_countries, reg_languages, reg_keywords = set(), set(), set(), set(), set()

                for movie, row in filmes_com_row:
                    self._cache_objetos(row, "genres", genre_cache, Genre, novos_generos)
                    self._cache_objetos(row, "production_companies", company_cache, ProductionCompany, novos_companies)
                    self._cache_objetos(row, "production_countries", country_cache, ProductionCountry, novos_countries)
                    self._cache_objetos(row, "spoken_languages", language_cache, SpokenLanguage, novos_languages)
                    self._cache_objetos(row, "keywords", keyword_cache, Keyword, novos_keywords)

                Genre.objects.bulk_create([Genre(name=n) for n in novos_generos if n not in genre_cache], ignore_conflicts=True)
                ProductionCompany.objects.bulk_create([ProductionCompany(name=n) for n in novos_companies if n not in company_cache], ignore_conflicts=True)
                ProductionCountry.objects.bulk_create([ProductionCountry(name=n) for n in novos_countries if n not in country_cache], ignore_conflicts=True)
                SpokenLanguage.objects.bulk_create([SpokenLanguage(name=n) for n in novos_languages if n not in language_cache], ignore_conflicts=True)
                Keyword.objects.bulk_create([Keyword(name=n) for n in novos_keywords if n not in keyword_cache], ignore_conflicts=True)

                genre_cache.update({g.name: g for g in Genre.objects.filter(name__in=novos_generos)})
                company_cache.update({c.name: c for c in ProductionCompany.objects.filter(name__in=novos_companies)})
                country_cache.update({c.name: c for c in ProductionCountry.objects.filter(name__in=novos_countries)})
                language_cache.update({l.name: l for l in SpokenLanguage.objects.filter(name__in=novos_languages)})
                keyword_cache.update({k.name: k for k in Keyword.objects.filter(name__in=novos_keywords)})

                for movie, row in filmes_com_row:
                    self._relacionar(row, movie, "genres", genre_cache, m2m_genres, movie_genres, "genre", reg_genres)
                    self._relacionar(row, movie, "production_companies", company_cache, m2m_companies, movie_companies, "productioncompany", reg_companies)
                    self._relacionar(row, movie, "production_countries", country_cache, m2m_countries, movie_countries, "productioncountry", reg_countries)
                    self._relacionar(row, movie, "spoken_languages", language_cache, m2m_languages, movie_languages, "spokenlanguage", reg_languages)
                    self._relacionar(row, movie, "keywords", keyword_cache, m2m_keywords, movie_keywords, "keyword", reg_keywords)

                movie_genres.objects.bulk_create(m2m_genres, batch_size=chunk_size, ignore_conflicts=True)
                movie_companies.objects.bulk_create(m2m_companies, batch_size=chunk_size, ignore_conflicts=True)
                movie_countries.objects.bulk_create(m2m_countries, batch_size=chunk_size, ignore_conflicts=True)
                movie_languages.objects.bulk_create(m2m_languages, batch_size=chunk_size, ignore_conflicts=True)
                movie_keywords.objects.bulk_create(m2m_keywords, batch_size=chunk_size, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS("✔️ Importacao finalizada com sucesso!"))

    @staticmethod
    def parse_date(value):
        if pd.isna(value):
            return None
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except Exception:
            return None

    @staticmethod
    def _cache_objetos(row, campo_csv, cache_dict, model_class, conjunto):
        raw = row.get(campo_csv)
        if pd.isna(raw):
            return

        nomes = [n.strip() for n in raw.split(",") if n.strip()]
        for nome in nomes:
            if nome not in cache_dict:
                conjunto.add(nome)

    @staticmethod
    def _relacionar(row, movie, campo_csv, cache_dict, destino, through_model, related_field, registro_set):
        raw = row.get(campo_csv)
        if pd.isna(raw):
            return

        nomes = [n.strip() for n in raw.split(",") if n.strip()]
        for nome in nomes:
            obj = cache_dict.get(nome)
            if not obj:
                continue
            chave = (movie.pk, obj.pk)
            if chave not in registro_set:
                registro_set.add(chave)
                destino.append(through_model(**{related_field: obj, "movie": movie}))
