import json
from django.http import response
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from gamerraterapi.models import Game, Player, Rating


class RatingTests(APITestCase):
    def setUp(self):
        """
        Create a new account
        """

        url = "/register"
        data = {
            "username": "RyanBeidenTest",
            "password": "test123!",
            "email": "test@test.com",
            "first_name": "Ryan",
            "last_name": "Beiden",
        }

        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.token = json_response['token']

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Create a Player Instance
        player = Player()
        player.user = User.objects.get(id=json_response['user_id'])
        player.save()

        # Create a Game Instance
        game = Game()
        game.title = "Monopoly"
        game.description = "A super good board game."
        game.designer = "Joe Smith"
        game.year_released = "1996-01-01"
        game.est_time_to_play = 25
        game.num_of_players = 12
        game.age_rec = 12
        game.image_url = ""
        game.player = player
        game.save()


    def test_create_rating(self):
        """
        Make sure we can create a rating
        """

        url = "/ratings"
        data = {
            "value": 7,
            "player": 1,
            "game": 1
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')

        json_response = json.loads(response.content)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(json_response["value"], 7)
        self.assertEqual(json_response["player"], 1)
        self.assertEqual(json_response["game"], 1)


    def test_change_game_rating(self):
        """
        Make sure we can change an existing rating.
        """

        # Create Rating
        rating = Rating()
        rating.value = 8
        rating.player_id = 1
        rating.game_id = 1
        rating.save()

        # Create Updated Rating Data
        data = {
            "value": 4,
            "player": 1,
            "game": 1
        }

        # Update new data to existing Rating
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(f"/ratings/{rating.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Get updated Rating
        response = self.client.get(f"/ratings/{rating.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response["value"], 4)
        self.assertEqual(json_response["player"], 1)
        self.assertEqual(json_response["game"], 1)