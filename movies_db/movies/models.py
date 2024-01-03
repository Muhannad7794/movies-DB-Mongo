from djongo import models
from bson import ObjectId


class Directors(models.Model):
    director_name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    director_date_of_birth = models.DateField()
    director_best_movies = models.CharField(max_length=215)
    awards = models.CharField(max_length=100)

    def __str__(self):
        return self.director_name

    class Meta:
        abstract = True  # This makes it a non-model type


class Studios(models.Model):
    name = models.CharField(max_length=100)
    founded = models.IntegerField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True  # This makes it a non-model type


class MovieInfo(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    release_year = models.IntegerField()
    director = models.EmbeddedField(
        model_container=Directors,
    )
    credits_score = models.FloatField()
    studio = models.EmbeddedField(
        model_container=Studios,
    )

    def __str__(self):
        return self.title


class Posters(models.Model):
    movie = models.ObjectIdField()  # Storing movie's id instead of foreign key
    poster = models.ImageField(upload_to="posters/")

    def __str__(self):
        return str(self.movie)


class DirectorsImages(models.Model):
    director = models.ObjectIdField()  # Storing director's name instead of foreign key
    picture = models.ImageField(upload_to="directors_images/")

    def __str__(self):
        return str(self.director)


class StudiosImages(models.Model):
    studio = models.ObjectIdField()  # Storing studio name instead of foreign key
    picture = models.ImageField(upload_to="studios_images/")

    def __str__(self):
        return str(self.studio)
