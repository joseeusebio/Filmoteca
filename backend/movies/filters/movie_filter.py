from django_filters import rest_framework as filters
from movies.models import Movie, Genre, ProductionCompany, ProductionCountry, SpokenLanguage, Keyword


class MovieFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr="istartswith")
    vote_average_min = filters.NumberFilter(field_name="vote_average", lookup_expr="gte")
    vote_average_max = filters.NumberFilter(field_name="vote_average", lookup_expr="lte")
    release_date__year = filters.NumberFilter(field_name="release_date", lookup_expr="year")
    genres = filters.ModelMultipleChoiceFilter(
        field_name="genres__name",
        to_field_name="name",
        queryset=Genre.objects.all(),
        conjoined=False
    )
    production_companies = filters.ModelMultipleChoiceFilter(
        field_name="production_companies__name",
        to_field_name="name",
        queryset=ProductionCompany.objects.all(),
        conjoined=False
    )
    production_countries = filters.ModelMultipleChoiceFilter(
        field_name="production_countries__name",
        to_field_name="name",
        queryset=ProductionCountry.objects.all(),
        conjoined=False
    )
    spoken_languages = filters.ModelMultipleChoiceFilter(
        field_name="spoken_languages__name",
        to_field_name="name",
        queryset=SpokenLanguage.objects.all(),
        conjoined=False
    )
    keywords = filters.ModelMultipleChoiceFilter(
        field_name="keywords__name",
        to_field_name="name",
        queryset=Keyword.objects.all(),
        conjoined=False
    )

    class Meta:
        model = Movie
        fields = []
