from django.apps import AppConfig


class ScoreboardConfig(AppConfig):
    name = 'scoreboard'

    def ready(self):
        import scoreboard.signals