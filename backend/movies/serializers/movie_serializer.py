from rest_framework import serializers
from movies.models import (
    Movie, Genre, ProductionCompany, ProductionCountry, SpokenLanguage, Keyword
)

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class ProductionCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionCompany
        fields = ['id', 'name']

class ProductionCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionCountry
        fields = ['id', 'name']

class SpokenLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpokenLanguage
        fields = ['id', 'name']

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ['id', 'name']

class MovieListSerializer(serializers.ModelSerializer):
    genres = serializers.StringRelatedField(many=True)
    poster_url = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'original_title', 'vote_average',
            'release_date', 'popularity', 'genres', 'poster_url'
        ]

    @staticmethod
    def get_poster_url(obj):
        return obj.poster_url

class MovieDetailSerializer(serializers.ModelSerializer):
    genres = serializers.StringRelatedField(many=True)
    production_companies = serializers.StringRelatedField(many=True)
    production_countries = serializers.StringRelatedField(many=True)
    spoken_languages = serializers.StringRelatedField(many=True)
    keywords = serializers.StringRelatedField(many=True)
    backdrop_url = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ['id']

    @staticmethod
    def get_backdrop_url(obj):
        return obj.backdrop_url