from django.db import models
from django.db.models.deletion import CASCADE

class Review(models.Model):

    content = models.CharField(max_length=500)
    game_id = models.ForeignKey("Game",
        on_delete=CASCADE,
        related_name="reviews",
        related_query_name="review"
    )
