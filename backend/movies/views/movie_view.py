from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from movies.models import Movie
from movies.serializers import MovieListSerializer, MovieDetailSerializer
from movies.filters.movie_filter import MovieFilter
from movies.pagination import CustomCursorPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Movie.objects.public()
    pagination_class = CustomCursorPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MovieFilter
    search_fields = ['title']
    ordering_fields = ['popularity', 'release_date', 'vote_average']
    ordering = ['-popularity']

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
            # ... e os demais
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

