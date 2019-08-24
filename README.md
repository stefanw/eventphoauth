# eventphoauth

## Local project setup

Start a local Redis server.

### Backend
```
python3 -m venv eventphoauth-env
source eventphoauth-env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Local project setup with Docker

```
docker-compose -f docker-compose.dev.yml up
```

## Deployment to Heroku

Add PostgreSQL-Addon and Redis-Addon.

```
git push heroku master
heroku config:set DEBUG=0
heroku config:set SECRET_KEY=<long securely random string>
heroku run python manage.py migrate
heroku restart
```

## Deployment with Docker

Copy `env.example` to `.env` and adjust values.

```
docker-compose up --build
```

The server will listen by default on port 8000.


## Admin interface

There's an admin interface at `/admin/`. You can create admin users like this:

```
python manage.py createsuperuser
```

