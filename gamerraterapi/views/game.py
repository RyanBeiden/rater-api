import os
import base64
from django.db import models
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.core.files.base import ContentFile
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import renderer_classes
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.db.models import Q
from gamerraterapi.models import Game, Category, Player, Rating

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Category
        fields = '__all__'
class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'title', 'description', 'designer', 'year_released', 'num_of_players', 'est_time_to_play', 'age_rec', 'image_url', 'player', 'categories', 'average_rating')
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

        search_text = self.request.query_params.get('q', None)
        sort_text = self.request.query_params.get('orderby', None)

        if search_text is not None:
            games = Game.objects.filter(
                Q(title__contains=search_text) |
                Q(description__contains=search_text) |
                Q(designer__contains=search_text)
            )

        elif sort_text is not None:
            games = Game.objects.order_by(f'{sort_text}')

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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk=None):
        try:
            post = Game.objects.get(pk=pk)
            post.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @receiver(models.signals.post_delete, sender=Game)
    def auto_delete_file_on_delete(sender, instance, **kwargs):
        # Deletes file from filesystem when corresponding `Game` object is deleted.

        if instance.image_url:
            if os.path.isfile(instance.image_url.path):
                os.remove(instance.image_url.path)


    def update(self, request, pk=None):
        player = Player.objects.get(user=request.auth.user)
        image_data = ''

        # Check for an image update
        game_image = Game.objects.get(pk=pk).image_url.name
        image_path = request.data['image_url'].split('media/')
        
        if image_path[-1] == game_image:
            image_data = image_path[1]

        # Format new post image
        elif request.data['image_url']:
            format, imgstr = request.data['image_url'].split(';base64,')
            ext = format.split('/')[-1]
            image_data = ContentFile(base64.b64decode(imgstr), name=f'.{ext}')

        game = Game.objects.get(pk=pk)
        game.title = request.data['title']
        game.description = request.data['description']
        game.designer = request.data['designer']
        game.year_released = request.data['year_released']
        game.est_time_to_play = request.data['est_time_to_play']
        game.num_of_players = request.data['num_of_players']
        game.age_rec = request.data['age_rec']
        game.image_url = image_data
        game.player = player
        game.save()

        categoryArr = request.data['categories']
        for category in categoryArr:
            categoryId = Category.objects.get(pk=category['id'])
            game.categories.add(categoryId)

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    @receiver(models.signals.pre_save, sender=Game)
    def auto_delete_file_on_change(sender, instance, **kwargs):
        # Deletes old file from filesystem when corresponding `Game` object is updated with new file.

        if not instance.pk:
            return False

        try:
            old_file = Game.objects.get(pk=instance.pk).image_url
        except Game.DoesNotExist:
            return False

        new_file = instance.image_url
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
