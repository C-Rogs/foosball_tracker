from django import forms
from .models import Player, Game, Match

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'is_active']

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['in_progress']

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['left_offense', 'left_defense', 'right_offense', 'right_defense', 'left_score', 'right_score']

    def clean(self):
        cleaned_data = super().clean()
        left_offense = cleaned_data.get("left_offense")
        left_defense = cleaned_data.get("left_defense")
        right_offense = cleaned_data.get("right_offense")
        right_defense = cleaned_data.get("right_defense")
        left_score = cleaned_data.get("left_score")
        right_score = cleaned_data.get("right_score")

        if left_offense == left_defense or right_offense == right_defense:
            raise forms.ValidationError("A player cannot be in both positions on the same team.")
        if left_offense in [right_offense, right_defense] or left_defense in [right_offense, right_defense]:
            raise forms.ValidationError("A player cannot be on both teams.")
        if left_score < 0 or left_score > 10 or right_score < 0 or right_score > 10:
            raise forms.ValidationError("Score must be between 0 and 10.")
