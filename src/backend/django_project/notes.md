
# REST API
1. Rest API is used to write the APIs from the frontend to the backend

# DJANGO
1. settings.py is used for the settins of the project
2. urls.py is used for the routing of the project
3. models.py is used for the models of the project (database entities)
4. views.py is used for the views of the project (logic of the project)
5. admin.py is used for the admin interface of the project
6. tests.py is used for the tests of the project
7. serializers.py is used for the serializers of the project (data handling)

- Other:
      - each app controls a part of the project (menu, oauth, etc)
      - after you make change to a certain app, you need to run python3 manage.py makemigrations and python3 manage.py migrate to update the database3

# ADMIN INTERFACE 
1. python manage.py createsuperuser
2. python manage.py runserver
3. go to http://127.0.0.1:8000/admin/ and login with the superuser credentials

# SCRIPTS
1. createuser.bash: creates a superuser
2. migrate.bash: makes migrations and runs the server (update and see changes)

# MODELS
1. Create a class that inherits the models.Model bae class
2. Each variable is a column with a datatype specified in models.
3. All datatypes are here: https://docs.djangoproject.com/en/5.1/ref/models/fields/
4. All primary keys are automatically added (integer, unique, auto_increment) (VERY IMPORTANT!)

