import json
from django.http import response
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from gamerraterapi.models import Game, Player, Category


class GameTests(APITestCase):
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

        #Create a Category Instance
        categories = Category()
        categories.category_name = "Strategy"
        categories.save()


    def test_create_game(self):
        """
        Make sure we can create a game
        """

        url = "/games"
        data = {
            "title": "Monopoly",
            "description": "A super good board game.",
            "designer": "IDK",
            "year_released": "1996-01-01",
            "est_time_to_play": 25,
            "num_of_players": 12,
            "age_rec": 12,
            "image_url": "",
            "player": 1,
            "categories": [1]
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(json_response["title"], "Monopoly")
        self.assertEqual(json_response["description"], "A super good board game.")
        self.assertEqual(json_response["designer"], "IDK")
        self.assertEqual(json_response["year_released"], "1996-01-01")
        self.assertEqual(json_response["est_time_to_play"], 25)
        self.assertEqual(json_response["num_of_players"], 12)
        self.assertEqual(json_response["age_rec"], 12)
        self.assertEqual(json_response["categories"], [1])