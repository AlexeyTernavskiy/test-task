# Django test task
###Install###

1. git clone **https://github.com/AlexYanovsky/test-task.git**
2. cd **test-task**
3. pip install -r **requirements_dev.txt**
4. change data base connnection in **src/core/settings/development.py** to

```
# DATABASE CONFIGURATION
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test_database',
    }
}
# END DATABASE CONFIGURATION
```
5. python manage.py migrate
6. python manage.py createsuperuser
7. python manage.py loaddata src/apps/product/fixtures/data.json
8. python manage.py test
9. python manage.py runserver --settings=src.core.settings.development
10. open you browser at http://127.0.0.1:8000
