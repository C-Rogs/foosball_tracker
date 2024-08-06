from rest_framework import serializers  
from games.models import Player, Match, Game 

class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        fields = ['date','in_progress', 'left_team_wins', 'right_team_wins' ]


class MatchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Match
        fields = ['game', 'left_offense','left_defense', 'right_offense', 'right_defense', 'left_score', 'right_score']

class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Player
        fields = ['name', 'is_active']