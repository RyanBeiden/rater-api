from django.core.exceptions import ValidationError
from django.urls.exceptions import Resolver404
from django.views.generic.base import View
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.decorators import renderer_classes
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from gamerraterapi.models import Game

class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        url = serializers.HyperlinkedIdentityField(
            view_name='game',
            lookup_field='id'
        )
        fields = ('id', 'url', 'title', 'description', 'designer', 'year_released', 'num_of_players', 'est_time_to_play', 'age_rec', 'image_url', 'categories')
        depth = 1


class GameViewSet(ViewSet):
    def retrieve(self, request, pk=None):

        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        games = Game.objects.all()

        serializer = GameSerializer(
            games, many=True, context={'request': request}
        )

        return Response(serializer.data)