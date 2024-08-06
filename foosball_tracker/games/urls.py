from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    GameDeleteView, MatchDeleteView, MatchDetailView, MatchListView, MatchUpdateView, home, PlayerListView, PlayerDetailView, PlayerCreateView, PlayerUpdateView,
    GameListView, GameDetailView, GameCreateView, GameUpdateView, add_match,
     mark_game_completed,SignupView
)
#CustomLoginView, CustomLogoutView,
urlpatterns = [
    path('', home, name='home'),
    path('players/', PlayerListView.as_view(), name='player-list'),
    path('players/<int:pk>/', PlayerDetailView.as_view(), name='player-detail'),
    path('players/new/', PlayerCreateView.as_view(), name='player-create'),
    #path('players/add/', PlayerCreateView.as_view(), name='player-create'),
    path('players/<int:pk>/edit/', PlayerUpdateView.as_view(), name='player-update'),
    
    path('games/', GameListView.as_view(), name='game-list'),
    path('games/<int:pk>/', GameDetailView.as_view(), name='game-detail'),
    path('games/new/', GameCreateView.as_view(), name='game-create'),
    #path('games/add/', GameCreateView.as_view(), name='game-create'),
    path('games/<int:pk>/delete/', GameDeleteView.as_view(), name='game-delete'),
    path('games/<int:pk>/edit/', GameUpdateView.as_view(), name='game-update'),
    path('games/<int:game_id>/add-match/', add_match, name='add-match'),
    path('games/<int:pk>/complete/', mark_game_completed, name='mark-game-completed'),
    
    path('matches/', MatchListView.as_view(), name='match-list'),
    path('matches/<int:pk>/', MatchDetailView.as_view(), name='match-detail'),
    path('matches/<int:pk>/edit/', MatchUpdateView.as_view(), name='match-update'),
    path('matches/<int:pk>/delete/', MatchDeleteView.as_view(), name='match-delete'),


    #path('login/', CustomLoginView.as_view(), name='login'),
    #path('logout/', CustomLogoutView.as_view(), name='logout'),
    #path('signup/', SignupView.as_view(), name='signup'),
    #path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    #path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    #path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    #path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
