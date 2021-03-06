# Generated by Django 3.2.8 on 2021-10-17 07:27

from django.db import migrations, models
import games.state


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.JSONField(decoder=games.state.GameStateDecoder, default=games.state.default_state, encoder=games.state.GameStateEncoder)),
            ],
        ),
    ]
