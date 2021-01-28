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

        # Create a Category Instance
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
            "designer": "Joe Smith",
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
        self.assertEqual(json_response["designer"], "Joe Smith")
        self.assertEqual(json_response["year_released"], "1996-01-01")
        self.assertEqual(json_response["est_time_to_play"], 25)
        self.assertEqual(json_response["num_of_players"], 12)
        self.assertEqual(json_response["age_rec"], 12)
        self.assertEqual(json_response["image_url"], None)
        self.assertEqual(json_response["player"]["id"], 1)


    def test_get_single_game(self):
        """
        Make sure we can get a single game
        """

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
        game.player_id = 1

        game.save()

        game.categories.add(Category.objects.get(pk=1))

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(f"/games/{game.id}")
        json_response = json.loads(response.content)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response["title"], "Monopoly")
        self.assertEqual(json_response["description"], "A super good board game.")
        self.assertEqual(json_response["designer"], "Joe Smith")
        self.assertEqual(json_response["year_released"], "1996-01-01")
        self.assertEqual(json_response["est_time_to_play"], 25)
        self.assertEqual(json_response["num_of_players"], 12)
        self.assertEqual(json_response["age_rec"], 12)
        self.assertEqual(json_response["image_url"], None)
        self.assertEqual(json_response["player"], {'id': 1, 'user': 1})
        self.assertEqual(json_response["categories"], [{'id': 1, 'category_name': 'Strategy'}])


    def test_get_all_games(self):
        """
        Make sure we can get all games
        """

        # Create a Game Instance
        for i in range(3):
            game = Game()
            game.title = "Monopoly"
            game.description = "A super good board game."
            game.designer = "Joe Smith"
            game.year_released = "1996-01-01"
            game.est_time_to_play = 25
            game.num_of_players = 12
            game.age_rec = 12
            game.image_url = ""
            game.player_id = 1

            game.save()

            game.categories.add(Category.objects.get(pk=1))

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get("/games")
        json_response = json.loads(response.content)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for i in range(3):
            self.assertEqual(json_response[i]["title"], "Monopoly")
            self.assertEqual(json_response[i]["description"], "A super good board game.")
            self.assertEqual(json_response[i]["designer"], "Joe Smith")
            self.assertEqual(json_response[i]["year_released"], "1996-01-01")
            self.assertEqual(json_response[i]["est_time_to_play"], 25)
            self.assertEqual(json_response[i]["num_of_players"], 12)
            self.assertEqual(json_response[i]["age_rec"], 12)
            self.assertEqual(json_response[i]["image_url"], None)
            self.assertEqual(json_response[i]["player"], {'id': 1, 'user': 1})
            self.assertEqual(json_response[i]["categories"], [{'id': 1, 'category_name': 'Strategy'}])