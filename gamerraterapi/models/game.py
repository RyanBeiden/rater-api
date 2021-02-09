import uuid
from cloudinary.models import CloudinaryField
from django.db import models
from django.contrib.auth.models import User
from .rating import Rating
from django.db.models.deletion import CASCADE
from django.utils.translation import gettext_lazy as _

class Game(models.Model):

    title = models.CharField(max_length=25)
    description = models.CharField(max_length=250)
    designer = models.CharField(max_length=25)
    year_released = models.DateField()
    est_time_to_play = models.IntegerField()
    num_of_players = models.IntegerField()
    age_rec = models.IntegerField()
    image_url = models.ImageField(_("Game Image"), blank=True, upload_to='games/')
    player = models.ForeignKey("Player",
        on_delete=CASCADE,
        related_name="games",
        related_query_name="game"
    )
    categories = models.ManyToManyField("Category")

    @property
    def average_rating(self):

        ratings = Rating.objects.filter(game=self)

        # Sum all of the ratings for the game
        total_rating = 0
        rating_count = 0

        for rating in ratings:
            total_rating += rating.value
            rating_count += 1
        
        if rating_count != 0:
            total_rating = round(total_rating / rating_count, 2)

        return total_rating
