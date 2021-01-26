from django.db import models
from django.db.models import CASCADE

class Rating(models.Model):
    value = models.IntegerField()
    player = models.ForeignKey("Player", 
        on_delete=CASCADE,
        related_name="ratings",
        related_query_name="rating")
    game = models.ForeignKey("Game", 
        on_delete=CASCADE,
        related_name="ratings",
        related_query_name="rating")