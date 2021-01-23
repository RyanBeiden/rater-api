import base64
from django.core.exceptions import ValidationError
from django.urls.exceptions import Resolver404
from django.views.generic.base import View
from django.core.files.base import ContentFile
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import renderer_classes
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import serializers
from gamerraterapi.models import Game, Category, Player, Rating

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Category
        fields = '__all__'
class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        url = serializers.HyperlinkedIdentityField(
            view_name='game',
            lookup_field='id'
        )
        fields = ('id', 'url', 'title', 'description', 'designer', 'year_released', 'num_of_players', 'est_time_to_play', 'age_rec', 'image_url', 'categories', 'average_rating')
        depth = 1


class GameViewSet(ModelViewSet):
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

    def create(self, request):
        player = Player.objects.get(user=request.auth.user)
        image_data = ''

        # Format new post image
        if request.data['image_url']:
            format, imgstr = request.data['image_url'].split(';base64,')
            ext = format.split('/')[-1]
            image_data = ContentFile(base64.b64decode(imgstr), name=f'.{ext}')

        game = Game()
        game.title = request.data['title']
        game.description = request.data['description']
        game.designer = request.data['designer']
        game.year_released = request.data['year_released']
        game.est_time_to_play = request.data['est_time_to_play']
        game.num_of_players = request.data['num_of_players']
        game.age_rec = request.data['age_rec']
        game.image_url = image_data
        game.player = player

        try:
            game.save()
            categoryArr = request.data['categories']
            for category in categoryArr:
                categoryId = Category.objects.get(pk=category)
                game.categories.add(categoryId)
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)
