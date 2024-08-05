from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Player, Game, Match
from .forms import PlayerForm, MatchForm, GameForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.views import View

def home(request):
    ongoing_games = Game.objects.filter(in_progress=True)
    completed_games = Game.objects.filter(in_progress=False)

    #summary for completed games
    game_summary = []
    for game in completed_games:
        matches = game.matches.all()
        left_team_wins = matches.filter(
            Q(left_score__gt=F('right_score'))
        ).count()
        right_team_wins = matches.filter(
            Q(right_score__gt=F('left_score'))
        ).count()
        game_summary.append({
            'game': game,
            'title': game.get_game_title(),
            'left_team_wins': left_team_wins,
            'right_team_wins': right_team_wins,
            'left_team': f"{game.matches.first().left_offense.name} & {game.matches.first().left_defense.name}",
            'right_team': f"{game.matches.first().right_offense.name} & {game.matches.first().right_defense.name}"
        })

    whitewashes = Match.objects.filter(
        Q(left_score=10, right_score=0) | Q(left_score=0, right_score=10)
    ).order_by('-date')[:5]

    top_players = Player.objects.filter(is_active=True).with_games_won()[:5]

    context = {
        'ongoing_games': ongoing_games,
        'completed_games': completed_games,
        'game_summary': game_summary,
        'whitewashes': whitewashes,
        'players': top_players
    }

    return render(request, 'games/home.html', context)


class PlayerListView(ListView):
    model = Player
    template_name = 'games/player_list.html'
    context_object_name = 'players'




class PlayerDetailView(DetailView):
    model = Player
    template_name = 'games/player_detail.html'


class PlayerCreateView(CreateView):
    model = Player
    form_class = PlayerForm
    template_name = 'games/player_form.html'
    success_url = reverse_lazy('player-list')


class PlayerUpdateView(LoginRequiredMixin, UpdateView):
    model = Player
    form_class = PlayerForm
    template_name = 'games/player_form.html'
    success_url = reverse_lazy('player-list')


class GameListView(ListView):
    model = Game
    template_name = 'games/game_list.html'
    context_object_name = 'games'


class GameDetailView(DetailView):
    model = Game

    template_name = 'games/game_detail.html'


class GameCreateView(CreateView):
    model = Game
    form_class = GameForm
    template_name = 'games/game_form.html'
    success_url = reverse_lazy('game-list')


class GameUpdateView(LoginRequiredMixin, UpdateView):
    model = Game
    form_class = GameForm
    template_name = 'games/game_form.html'
    success_url = reverse_lazy('game-list')


def mark_game_completed(request, pk):
    game = get_object_or_404(Game, pk=pk)
    game.in_progress = False
    game.save()
    return redirect('game-detail', pk=pk)


def add_match(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    if not game.in_progress:
        return redirect('game-detail', pk=game.id)  # Or show an error message

    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            match = form.save(commit=False)
            match.game = game
            match.save()
            return redirect('game-detail', pk=game.id)
    else:
        form = MatchForm()
    return render(request, 'games/add_match.html', {'form': form, 'game': game})

'''
class CustomLoginView(LoginView):
    template_name = 'games/login.html'


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')
'''

class SignupView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))
        return render(request, 'registration/signup.html', {'form': form})
