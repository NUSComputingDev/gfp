from django.contrib.auth import login
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm


def login_view(request):
    form = AuthenticationForm()

    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.POST:
        form = AuthenticationForm(request, request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return HttpResponseRedirect('/')

    return render(request, 'players/login.html', {'form': form})