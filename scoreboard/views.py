from django.shortcuts import render
from .models import Game
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
def scoreboard_view(request):
	games = Game.objects.all()
	return render(request, 'scoreboard/scoreboard.html', {'games': games})

@permission_required('scoreboard.can_update')
@login_required
def scoreboard_update(request):
	if request.method =='POST':
		# received an update, let's check
		pass
	else:
		# show form to facilitator
		pass

	return render(request, 'scoreboard/update.html')
