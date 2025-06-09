from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models.functions import ExtractYear

from movies.models import Movie, Genre, ProductionCompany, ProductionCountry, Keyword, SpokenLanguage
from movies.serializers import MovieListSerializer, MovieDetailSerializer, FormOptionsSerializer
from movies.filters.movie_filter import MovieFilter
from movies.pagination import CustomPageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MovieFilter
    search_fields = ['title']
    ordering_fields = ['popularity', 'release_date', 'vote_average']
    ordering = ['-popularity']

    def get_queryset(self):
        qs = Movie.objects.public().only(
            'id', 'title', 'original_title', 'vote_average',
            'release_date', 'popularity', 'poster_path'
        )

        if self.action == 'retrieve':
            return Movie.objects.public().prefetch_related(
                'genres', 'production_companies', 'production_countries',
                'spoken_languages', 'keywords'
            )

        if self.action == 'list':
            if 'title' in self.request.query_params and self.request.query_params['title'].strip():
                return qs
            return qs.prefetch_related('genres')

        return Movie.objects.public()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MovieDetailSerializer
        return MovieListSerializer

    @swagger_auto_schema(
        operation_summary="Listar filmes com filtros, busca e ordenação",
        manual_parameters=[
            openapi.Parameter("title", openapi.IN_QUERY, description="Título parcial", type=openapi.TYPE_STRING),
            openapi.Parameter("vote_average_min", openapi.IN_QUERY, description="Nota mínima",
                              type=openapi.TYPE_NUMBER),
        ]
    )
    def list(self, request, *args, **kwargs):
        """Lista paginada de filmes com filtros, ordenação e busca parcial por título."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Detalhar informações de um filme",
        operation_description="Retorna todos os campos disponíveis de um filme específico, incluindo seus relacionamentos."
    )
    def retrieve(self, request, *args, **kwargs):
        """Detalhes completos de um único filme"""
        return super().retrieve(request, *args, **kwargs)

    @action(detail=False, methods=["get"], url_path="form-options")
    def form_options(self, request):
        genres = list(Genre.objects.order_by("name").values_list("name", flat=True))
        countries = list(ProductionCountry.objects.order_by("name").values_list("name", flat=True))
        languages = list(SpokenLanguage.objects.order_by("name").values_list("name", flat=True))

        years = (
            Movie.objects.exclude(release_date=None)
            .annotate(year=ExtractYear("release_date"))
            .values_list("year", flat=True)
            .distinct()
        )

        return Response(FormOptionsSerializer({
            "genres": genres,
            "production_countries": countries,
            "spoken_languages": languages,
            "years": sorted(years, reverse=True),
        }).data)
