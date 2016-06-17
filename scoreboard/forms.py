from django.forms import ModelForm
from .models import Score
from games.models import Guess

# Form for scoreboard
class ScoreForm(ModelForm):
    class Meta:
        model = Score
        fields = ['score']

# Form for players who are guessing for a session
class GuessingForm(ModelForm):
    class Meta:
        model = Guess
        fields = ['guess']
