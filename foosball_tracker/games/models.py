from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Sum, Q, F, Count, Case, When, IntegerField, Value

class Player(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def games_won(self):
        return Match.objects.filter(
            (Q(left_offense=self) | Q(left_defense=self)) & Q(left_score__gt=F('right_score')) |
            (Q(right_offense=self) | Q(right_defense=self)) & Q(right_score__gt=F('left_score'))
        ).count()

    def total_points(self):
        left_points = Match.objects.filter(
            Q(left_offense=self) | Q(left_defense=self)
        ).aggregate(total=Sum('left_score'))['total'] or 0
        right_points = Match.objects.filter(
            Q(right_offense=self) | Q(right_defense=self)
        ).aggregate(total=Sum('right_score'))['total'] or 0
        return left_points + right_points

    def win_ratio(self):
        total_matches = Match.objects.filter(
            Q(left_offense=self) | Q(left_defense=self) | Q(right_offense=self) | Q(right_defense=self)
        ).count()
        return self.games_won() / total_matches if total_matches else 0

    def best_position(self):
        defense_wins = Match.objects.filter(left_defense=self, left_score__gt=F('right_score')).count() + \
                       Match.objects.filter(right_defense=self, right_score__gt=F('left_score')).count()
        offense_wins = Match.objects.filter(left_offense=self, left_score__gt=F('right_score')).count() + \
                       Match.objects.filter(right_offense=self, right_score__gt=F('left_score')).count()
        return 'Defense' if defense_wins > offense_wins else 'Offense'

    def most_successful_teammate(self):        

        # Check if the player has any matches
        if not Match.objects.filter(
            Q(left_offense=self) | Q(left_defense=self) | Q(right_offense=self) | Q(right_defense=self)
        ).exists():
            return None  # No matches found, return None

        # Annotate teammates and count matches and wins with the player
        teammates = Player.objects.exclude(id=self.id).annotate(
            total_matches_with=Count(
                Case(
                    When(Q(left_offense_matches__left_defense=self) | Q(left_offense_matches__right_offense=self) | Q(left_offense_matches__right_defense=self) |
                        Q(left_defense_matches__left_offense=self) | Q(left_defense_matches__right_offense=self) | Q(left_defense_matches__right_defense=self) |
                        Q(right_offense_matches__left_offense=self) | Q(right_offense_matches__left_defense=self) | Q(right_offense_matches__right_defense=self) |
                        Q(right_defense_matches__left_offense=self) | Q(right_defense_matches__left_defense=self) | Q(right_defense_matches__right_offense=self),
                        then=1),
                    output_field=IntegerField()
                )
            ),
            win_count=Count(
                Case(
                    When(Q(left_offense_matches__left_defense=self, left_offense_matches__left_score__gt=F('left_offense_matches__right_score')) |
                        Q(left_offense_matches__right_offense=self, left_offense_matches__left_score__gt=F('left_offense_matches__right_score')) |
                        Q(left_offense_matches__right_defense=self, left_offense_matches__left_score__gt=F('left_offense_matches__right_score')) |
                        Q(left_defense_matches__left_offense=self, left_defense_matches__left_score__gt=F('left_defense_matches__right_score')) |
                        Q(left_defense_matches__right_offense=self, left_defense_matches__left_score__gt=F('left_defense_matches__right_score')) |
                        Q(left_defense_matches__right_defense=self, left_defense_matches__left_score__gt=F('left_defense_matches__right_score')) |
                        Q(right_offense_matches__left_offense=self, right_offense_matches__right_score__gt=F('right_offense_matches__left_score')) |
                        Q(right_offense_matches__left_defense=self, right_offense_matches__right_score__gt=F('right_offense_matches__left_score')) |
                        Q(right_offense_matches__right_defense=self, right_offense_matches__right_score__gt=F('right_offense_matches__left_score')) |
                        Q(right_defense_matches__left_offense=self, right_defense_matches__right_score__gt=F('right_defense_matches__left_score')) |
                        Q(right_defense_matches__left_defense=self, right_defense_matches__right_score__gt=F('right_defense_matches__left_score')) |
                        Q(right_defense_matches__right_offense=self, right_defense_matches__right_score__gt=F('right_defense_matches__left_score')),
                        then=1),
                    output_field=IntegerField()
                )
            )
        ).annotate(
            win_ratio=F('win_count') * 1.0 / F('total_matches_with')
        ).order_by('-win_ratio')

        # Get the top teammate
        if teammates.exists():
            return teammates.first()
        else:
            return None
        


class Game(models.Model):
    date = models.DateTimeField(default=timezone.now)
    in_progress = models.BooleanField(default=True)  # To track ongoing games
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    left_team_wins = models.IntegerField(default=0)
    right_team_wins = models.IntegerField(default=0)
    #left_offense = models.ForeignKey(Player, related_name='left_offense_games', on_delete=models.CASCADE)
    #left_defense = models.ForeignKey(Player, related_name='left_defense_games', on_delete=models.CASCADE)
    #right_offense = models.ForeignKey(Player, related_name='right_offense_games', on_delete=models.CASCADE)
    #right_defense = models.ForeignKey(Player, related_name='right_defense_games', on_delete=models.CASCADE)

    def __str__(self):
        return f"Game on {self.date.date()}"
    
    def get_first_match_players(self):
        first_match = self.matches.first()
        if first_match:
            return (first_match.left_offense, first_match.left_defense, first_match.right_offense, first_match.right_defense)
        else:
            return ("Unknown Player", "Unknown Player", "Unknown Player", "Unknown Player")

    def get_game_title(self):
        left_offense, left_defense, right_offense, right_defense = self.get_first_match_players()
        return f"{left_offense} & {left_defense} vs {right_offense} & {right_defense}"
    
    def mark_as_completed(self):
        self.in_progress = False
        self.save()

class Match(models.Model):
    game = models.ForeignKey(Game, related_name='matches', on_delete=models.CASCADE)
    left_offense = models.ForeignKey(Player, related_name='left_offense_matches', on_delete=models.CASCADE)
    left_defense = models.ForeignKey(Player, related_name='left_defense_matches', on_delete=models.CASCADE)
    right_offense = models.ForeignKey(Player, related_name='right_offense_matches', on_delete=models.CASCADE)
    right_defense = models.ForeignKey(Player, related_name='right_defense_matches', on_delete=models.CASCADE)
    left_score = models.IntegerField()
    right_score = models.IntegerField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.game} - {self.left_score} vs {self.right_score}"

    def winner(self):
        if self.left_score > self.right_score:
            return 'Left'
        elif self.right_score > self.left_score:
            return 'Right'
        return 'Draw'

    def clean(self):
        super().clean()
        if self.left_score < 0 or self.left_score > 10 or self.right_score < 0 or self.right_score > 10:
            raise ValidationError('Score must be between 0 and 10.')
        if self.left_score != 10 and self.right_score != 10:
            raise ValidationError('One team must score 10 to win!')
        if self.left_score == 10 and self.right_score == 10:
            raise ValidationError('Only one team can win!')
        if self.left_offense == self.left_defense or self.right_offense == self.right_defense:
            raise ValidationError('A player cannot be on both positions in the same team.')
        if self.left_offense in [self.right_offense, self.right_defense] or self.left_defense in [self.right_offense, self.right_defense]:
            raise ValidationError('A player cannot be on both teams.')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.winner() == 'Left':
            self.game.left_team_wins += 1
        elif self.winner() == 'Right':
            self.game.right_team_wins += 1
        self.game.save()
