from django.core.exceptions import ValidationError
from django.http.response import HttpResponseServerError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from gamerraterapi.models import Game, Rating, Player

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'value', 'player', 'game')


class RatingViewSet(ViewSet):
    def list(self, request):
        ratings = Rating.objects.all()

        game_id = self.request.query_params.get('game_id', None)
        player_id = request.auth.user

        if game_id is not None:
            game_ratings = ratings.filter(game=game_id)
            ratings = game_ratings.filter(player=player_id.id)

        serializer = RatingSerializer(
            ratings, many=True, context={'request': request}
        )

        return Response(serializer.data)

    def create(self, request):

        game = Game.objects.get(pk=request.data['game'])

        rating = Rating()
        rating.value = request.data['value']
        rating.player = Player.objects.get(user=request.auth.user)
        rating.game = game

        try:
            rating.save()
            serializer = RatingSerializer(rating, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):

        game = Game.objects.get(pk=request.data['game'])

        rating = Rating.objects.get(pk=pk)
        rating.value = request.data['value']
        rating.player = Player.objects.get(user=request.auth.user)
        rating.game = game

        rating.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)