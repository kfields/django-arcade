# Django Arcade :snake: :video_game:

This repo serves as a blueprint/starter-kit to develop game servers and clients using GraphQL

Initially it uses [Django](https://www.djangoproject.com/) as the game server and [Python Arcade](https://api.arcade.academy/) for the client

The first game to be implemented is Tic-Tac-Toe

## Git

```bash
git clone https://github.com/kfields/django-arcade
cd django-arcade
poetry shell
```

## Server

```bash
cd server
poetry install
```

### First Time

```
./bin/setup
```

### After that ...

```
./bin/dev
```

### Start from Scratch:  Delete the database and migrations, and re-run setup

```
./bin/nuke
```

## Client

```bash
cd client
poetry install
python client
```

## Experiments

```bash
cd experiments
poetry install
python counter.py
```

## Special Thanks
Django Bulma app from:  https://github.com/lemonsaurus/django-simple-bulma

Some more stuff from:  https://github.com/python-discord/site