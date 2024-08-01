# Generated by Django 5.0.7 on 2024-08-01 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0008_alter_game_in_progress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='is_completed',
        ),
        migrations.AddField(
            model_name='game',
            name='left_team_wins',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='game',
            name='right_team_wins',
            field=models.IntegerField(default=0),
        ),
    ]
