import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.utils.translation import gettext_lazy as _

class Game(models.Model):

    def upload_to(instance, filename):
        return f"games/{instance.player.id}-{uuid.uuid4()}"

    title = models.CharField(max_length=25)
    description = models.CharField(max_length=250)
    designer = models.CharField(max_length=25)
    year_released = models.DateField()
    est_time_to_play = models.IntegerField()
    num_of_players = models.IntegerField()
    age_rec = models.IntegerField()
    image_url = models.ImageField(_("Game Image"), blank=True, upload_to=upload_to)
    player = models.ForeignKey("Player",
        on_delete=CASCADE,
        related_name="games",
        related_query_name="game"
    )
    categories = models.ManyToManyField("Category")
