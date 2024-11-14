
# DATA FLOW
1. User signs in. 
2. User creates a post (logger gets triggered)
3. User uploads pdf 
4. Menu related tables get filled  


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
1. To access the admin interface activate server (see scripts folder) and go to http://127.0.0.1:8000/admin/ 

# SCRIPTS
1. createuser.bash: creates a superuser
2. migrate.bash: makes migrations and runs the server (update and see changes)
3. startServer.bash: runs the server

# MODELS
1. Create a class that inherits the models.Model bae class
2. Each variable is a column with a datatype specified in models.
3. All datatypes are here: https://docs.djangoproject.com/en/5.1/ref/models/fields/
4. All primary keys are automatically added 
5. Each model has to be specified within admin.py
6. __str__: represents the object name in the admin interface

# CONTRIBUTING TO THE ADMIN INTERFACE
1. Make sure u understand the prior concepts. Have installed all the dependencies
2. Create a file named .env withing the outermost django_project folder 
3. Populate the .env file with the following keys:
      # LOCAL MYSQL
      DB_HOST="localhost"
      DB_PASSWORD="yourpassword"
      DB_USER="root"
      DB_NAME="database_name"
      DB_PORT="3306"

      # OPENAI
      OPENAI_API_KEY="your_openai_api_key"
4. Create a superuser using the createuser.bash script
5. Run the migrate.bash script to update the database
7. Go to http://127.0.0.1:8000/admin/ to access the admin interface
