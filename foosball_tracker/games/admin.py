from django.contrib import admin
from .models import Player, Team, Game, Round

admin.site.register(Player)
admin.site.register(Team)
admin.site.register(Game)
admin.site.register(Round)
