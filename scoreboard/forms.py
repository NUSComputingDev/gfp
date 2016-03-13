from django.forms import ModelForm
from .models import Score

# Form for scoreboard
class ScoreForm(ModelForm):
    class Meta:
        model = Score
        fields = ['score']
