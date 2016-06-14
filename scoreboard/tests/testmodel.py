from django.test import TestCase
from django.contrib.auth.models import User

from scoreboard import models
from players.models import Player

import unittest


class ScoreboardTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        """Sets up the testing environment"""
        cls.setup_users()
        cls.player = Player.objects.create(user=cls.player_user)
        cls.normal_game = models.Game.objects.create(name='Normal Game',
                                                     is_active=True)

    def create_test_gamesession(self, game_type1=models.Game.NORMAL):
        """
        Creates a GameSession for tests that do not explicitly test
        the correctness of GameSession
        """
        return models.GameSession.objects.create(game_master=self.gm_user,
                                                 game=self.normal_game)

    def create_test_gamemaster(self, prefix_username):
        """
        Creates a dummy GameMaster for testing
        """
        return User.objects.create_user('{}-test'.format(prefix_username))

    def test_basic_scoring(self):
        """
        Test if player's score is recorded correctly
        Test Coverage: Relations of Player, Score and Session. Integrity of
        score storage
        """
        game_session = self.create_test_gamesession()

        score = game_session.score_set.create(player=self.player,
                                              score=750)

        self.assertEqual(self.player.score_set.get(pk=score.id), score,
                         "Basic score relation for player")

    def test_aggregate_scoring(self):
        """
        Test if a player's aggregate score is recorded correctly
        Test Coverage: Calculation of aggregate score and integrity of store
        """
        game_session = self.create_test_gamesession(models.Game.GUESSING)
        aggregate = models.AggregatedScore.objects.create(game_session=game_session,
                                                          player=self.player)

        scoring_data = [[25, 100], [25, 50], [25, 40], [25, 30]]
        expected_score = 55

        for partial_score in scoring_data:
            fake_gm = self.create_test_gamemaster(partial_score[1])
            models.PartialScore.objects.create(aggregated_score=aggregate,
                                               game_master=fake_gm,
                                               percentage=partial_score[0],
                                               score=partial_score[1])

        scored = models.AggregatedScore.objects.get(pk=aggregate.id)
        self.assertEqual(expected_score, scored.score,
                         "Basic Aggregate Scoring test")

    @classmethod
    def setup_users(cls):
        """Creates users necessary for testing purposes"""
        cls.player_user = User.objects.create_user('player')
        cls.gm_user = User.objects.create_user('gamemaster')

    @classmethod
    def tearDownClass(cls):
        cls.teardown_users()
        cls.player.delete()

    @classmethod
    def teardown_users(cls):
        """Removes users created using setup_users"""
        cls.player_user.delete()
        cls.gm_user.delete()