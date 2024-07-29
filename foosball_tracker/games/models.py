from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    player1 = models.ForeignKey(Player, related_name='teams_as_player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey(Player, related_name='teams_as_player2', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.player2:
            return f'{self.player1} & {self.player2}'
        return str(self.player1)

class Game(models.Model):
    team1 = models.ForeignKey(Team, related_name='games_as_team1', on_delete=models.CASCADE)
    team2 = models.ForeignKey(Team, related_name='games_as_team2', on_delete=models.CASCADE)
    best_of = models.IntegerField(default=3)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.team1} vs {self.team2} on {self.date}'

class Round(models.Model):
    game = models.ForeignKey(Game, related_name='rounds', on_delete=models.CASCADE)
    team1_score = models.IntegerField()
    team2_score = models.IntegerField()
    side = models.CharField(max_length=50)
    round_number = models.IntegerField()

    def __str__(self):
        return f'Round {self.round_number}: {self.team1_score}-{self.team2_score} on {self.side}'
