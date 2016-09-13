# Django test task
###Install###

1. git clone **https://github.com/digitalashes/test-task.git**
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

####Description:
#####Create django-project with one application in git repositories
-   Add the model `Category` with fields
    -   name
    -   slug
    -   description
-   Add the model `Product` with fields
    -   name
    -   slug
    -   description
    -   price
    -   created\_at
    -   modified\_at
-   Add all the models in the admin panel (all of the objects to be displayed on the field name)
-   Create a page with a list of categories, display all fields and links to page `(/products/)`
-   Create a page with a list of products of parent category, display all fields and links to page `(/products/<category_slug>/)`
-   Create a product page display name, description, and price of the product `(/products/<category_slug>/<product_slug>/)`
-   Create a page with a list of products added in the last 24 hours, make this page accessible only to logged users
-   Use migrations
-   Write unit tests for one page
-   Use MySQL or PostgreSQL (at choice)
-   Make two settings available: for development and for deploy
-   All pages should be available on the links
-   Create a base template file and extend from it all the other
-   Add a file with dependencies
-   Basic language - English
