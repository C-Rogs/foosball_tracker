# Generated by Django 5.0.7 on 2024-07-30 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_remove_team_player1_remove_team_player2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='round',
            name='round_number',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='round',
            name='score_team1',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='round',
            name='score_team2',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='round',
            name='side_played',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='round',
            name='winning_team',
            field=models.CharField(blank=True, choices=[('team1', 'Team 1'), ('team2', 'Team 2')], max_length=10, null=True),
        ),
    ]
