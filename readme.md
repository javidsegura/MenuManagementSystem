# Description

Menu management system for restaurant.Powered by AI.

# Contributions

Please, create your own branch and send a pull request. Make sure you have installed all the dependecies in the requirements.txt file.

1. Make sure u understand the main parts of the codebase. Have installed all the dependencies
2. Create a file named .env withing the outermost django_project folder 
3. Populate the .env file with the following keys:
      - DB_HOST="localhost"
      - DB_PASSWORD="yourpassword"
      - DB_USER="root"
      - DB_NAME="database_name"
      - DB_PORT="3306"
      - OPENAI_API_KEY="your_openai_api_key"
4. Create a superuser using the createuser.bash script
5. Run the migrate.bash script to update the database
7. Go to http://127.0.0.1:8000/admin/ to access the admin interface


# ETL Pipeline
ETL stands for Extract, Transform, Load.

1. Upload PDF  ✅
2. Send to GPT ✅
3. Add to DB ✅


# Procedure 
0. Set up database
      0.1 Create schema
      0.2 Plan index strategy
1. Set-up django project
2. Crate AI query 
3. Set up queries 
4. Set up logger
5. Extensive documentation
6. Presentation
7. Create test cases and sample queries  

# TESTING
1. Create a user 
2 Create a menu_version




# Extra features
0. Provide a simple UI for the user
1. Deploy to the cloud
2. Implement database triggers
3. Add full-text search
4. Create materialized views
5. Add menu version control
6. Permissions in SQL
6.5 HTML extracion
8. Improve security, and effficency
9. Deploy to the cloud
