from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from gamerraterapi.models import Game, Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'content', 'game_id')


class ReviewViewSet(ViewSet):
    def retrieve(self, request, pk=None):

        try:
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(review, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        reviews = Review.objects.all()

        game_id = self.request.query_params.get('game_id', None)

        if game_id is not None:
            reviews = reviews.filter(game_id=game_id)

        serializer = ReviewSerializer(
            reviews, many=True, context={'request': request}
        )

        return Response(serializer.data)

    def create(self, request):
        game = Game.objects.get(pk=request.data['game_id'])

        review = Review()
        review.content = request.data['content']
        review.game_id = game

        try:
            review.save()
            serializer = ReviewSerializer(review, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)