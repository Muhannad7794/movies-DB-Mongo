# movies/serializers.py
from rest_framework import serializers
from .models import (
    MovieInfo,
    Directors,
    Studios,
    Posters,
    DirectorsImages,
    StudiosImages,
)


# Serializers for embedded models
class DirectorsSerializer(serializers.Serializer):
    director_name = serializers.CharField(max_length=100)
    nationality = serializers.CharField(max_length=100)
    director_date_of_birth = serializers.DateField()
    director_best_movies = serializers.CharField(max_length=215)
    awards = serializers.CharField(max_length=100)


class StudiosSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    founded = serializers.IntegerField()
    location = serializers.CharField(max_length=100)


# Main Model Serializers
class MovieInfoSerializer(serializers.ModelSerializer):
    director = DirectorsSerializer()
    studio = StudiosSerializer()
    poster_url = serializers.SerializerMethodField()

    class Meta:
        model = MovieInfo
        fields = "__all__"

    def get_poster_url(self, obj):
        poster = Posters.objects.filter(movie=obj.pk).first()
        if poster and poster.poster:
            return self.context["request"].build_absolute_uri(poster.poster.url)
        return None


class PostersSerializer(serializers.ModelSerializer):
    poster = serializers.ImageField(use_url=True)

    class Meta:
        model = Posters
        fields = "__all__"


class DirectorsImagesSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(use_url=True)

    class Meta:
        model = DirectorsImages
        fields = "__all__"


class StudiosImagesSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(use_url=True)

    class Meta:
        model = StudiosImages
        fields = "__all__"
