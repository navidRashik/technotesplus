# TechNotes Plus (A template project)
## How to run it
```
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

after running the please look into flowing link for documentation
```
http://127.0.0.1:8000/swagger/
http://127.0.0.1:8000/redoc/#operation/notes_notes_create

```

## things to add:
will add redis,rabbitmq and celery usage and other useful drf features 


if you run the project and go to
127.0.0.1:8000/swagger.json
you will get OpenAPI  auto-generated doc and import it to postman or insomnia

again 127.0.0.1:8000/swagger/
127.0.0.1:8000/redoc
going to this URL you will get user interface