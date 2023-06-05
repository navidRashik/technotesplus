# TechNotes Plus (A template project)

The purpose of this project is to keep day to day small code segments here so that when needed they can be found easily.

# project detail

this is a note keeping app with limited functionality of keeping private/pbulic note and share that with other user.

## How to run it

need docker in your environment. pls download it before running.

```
docker-compose up
```

after running the please look into flowing link for documentation

```
http://127.0.0.1:8000/swagger/
http://127.0.0.1:8000/redoc/
```

## things added

drf, celery shared task

## things to add

will add testing, signals, caching, message broker, django-channel usage and other useful drf features.

if you run the project and go to
127.0.0.1:8000/swagger.json
you will get OpenAPI  auto-generated doc and import it to postman or insomnia
