from games.models import Player, Game, Match
from rest_framework import permissions, viewsets
from api.serializers import GameSerializer, MatchSerializer, PlayerSerializer

class GameViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows games to be viewed or edited.
    """
    queryset = Game.objects.all().order_by('-date')
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]


class MatchViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows matches to be viewed or edited.
    """
    queryset = Match.objects.all().order_by('date')
    serializer_class = MatchSerializer
    permission_classes = [permissions.IsAuthenticated]


class PlayerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows players to be viewed or edited.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [permissions.IsAuthenticated]