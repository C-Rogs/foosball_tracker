from django.shortcuts import render, get_object_or_404
from .models import Game

def index(request):
    games = Game.objects.all()
    return render(request, 'games/index.html', {'games': games})
