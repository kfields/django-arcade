# Generated by Django 3.2.8 on 2021-10-17 07:27

from django.db import migrations, models
import django.db.models.deletion
import players.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, 'Joined'), (2, 'Ready')], default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('symbol', models.CharField(max_length=1)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.game')),
                ('prev', models.OneToOneField(blank=True, null=True, on_delete=models.SET(players.models.get_prev_player), related_name='next', to='players.player')),
            ],
        ),
    ]
