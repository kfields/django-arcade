# Django Arcade

## Git

```bash
git clone https://github.com/kfields/django-arcade
cd django-arcade
```

## Server

```bash
cd server
poetry shell
poetry install
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
python manage.py runserver
```

## Examples

```bash
cd examples
poetry shell
poetry install
python hello.py
```