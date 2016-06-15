from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth.models import User

from scoreboard import models as sb_model
from players.models import Player
from games import models


class GuessModelTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        """Sets up the testing environment"""
        cls.setUpUsers()
        cls.player = Player.objects.create(user=cls.player_user)
        guessing_game_data = {'name': 'Game',
                              'game_type': sb_model.Game.GUESSING,
                              'is_active': True}
        cls.guessing_game = sb_model.Game.objects.create(**guessing_game_data)

    @classmethod
    def setUpUsers(cls):
        """Creates users necessary for testing purposes"""
        cls.player_user = User.objects.create_user('player')
        cls.gm_user = User.objects.create_user('gamemaster')

    def create_game_session(self, game, is_active=True):
        """Creates a GameSession for testing"""
        return sb_model.GameSession.objects.create(game_master=self.gm_user,
                                                   game=game,
                                                   is_active=is_active)

    def test_create_guess(self):
        """
        Test if we are able to create a Guess object
        Test Coverage:
            - Creation of Guess object
            - Data store integrity
            - Relations
            - Automated Fields
        """
        game_session = self.create_game_session(self.guessing_game)
        guess = models.Guess.objects.create(guess=145,
                                            game_session=game_session,
                                            player=self.player)

        guess_db_data = models.Guess.objects.get(pk=guess.pk)

        self.assertEqual(guess_db_data, guess,
                         "Test if Guess can be stored in database")
        self.assertEqual(game_session.guess_set.get(pk=guess.pk), guess,
                         "Test if Guess has a relation with GameSession")
        self.assertIsNotNone(guess_db_data.guessed_on,
                             "Test if Guess has a timestamp")

    def test_create_guess_inactive_gamesession(self):
        """
        Test if we are prevented from creating a Guess object linked to
        an inactive game session.

        Test Coverage:
            - Checks on GameSession validity
            - Data store integrity when preventing addition
        """
        game_session = self.create_game_session(self.guessing_game, False)

        guess = models.Guess.objects.create(guess=144,
                                            game_session=game_session,
                                            player=self.player)
        with self.assertRaises(guess.DoesNotExist):
            guess_db_data = models.Guess.objects.get(pk=guess.pk)

        self.assertIsNone(guess.pk, "Guess save does not affect primary keys")

    @classmethod
    def tearDownClass(cls):
        """Destroys the testing environment"""
        cls.tearDownUsers()
        cls.player.delete()
        cls.guessing_game.delete()

    @classmethod
    def tearDownUsers(cls):
        """Removes users created using setup_users"""
        cls.player_user.delete()
        cls.gm_user.delete()
