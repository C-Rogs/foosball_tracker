from django.urls import path
from .views import (
    home, PlayerListView, PlayerDetailView, PlayerCreateView, PlayerUpdateView,
    GameListView, GameDetailView, GameCreateView, GameUpdateView, add_match,
    CustomLoginView, CustomLogoutView, mark_game_as_completed,SignupView
)

urlpatterns = [
    path('', home, name='home'),
    path('players/', PlayerListView.as_view(), name='player-list'),
    path('players/<int:pk>/', PlayerDetailView.as_view(), name='player-detail'),
    path('players/new/', PlayerCreateView.as_view(), name='player-create'),
    path('players/<int:pk>/edit/', PlayerUpdateView.as_view(), name='player-update'),
    
    path('games/', GameListView.as_view(), name='game-list'),
    path('games/<int:pk>/', GameDetailView.as_view(), name='game-detail'),
    path('games/new/', GameCreateView.as_view(), name='game-create'),
    path('games/<int:pk>/edit/', GameUpdateView.as_view(), name='game-update'),
    path('games/<int:game_id>/add-match/', add_match, name='add-match'),
    path('games/<int:pk>/complete/', mark_game_as_completed, name='mark-game-completed'),


    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),

]
