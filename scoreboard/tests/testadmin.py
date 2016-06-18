from django.test import TestCase
from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.sites import AdminSite

import scoreboard.admin


class MockRequest(object):
    pass

class MockGameMaster(object):
    """Mocks a GameMaster user"""
    is_staff = False
    def has_perm(self, perm):
        return True

class MockSuperUser(object):
    """Mocks an Administrator user"""
    is_staff = True
    def has_perm(self, perm):
        return True

request = MockRequest()

class ScoreboardAdminTest(TestCase):

    def setUp(self):

        self.site = AdminSite()