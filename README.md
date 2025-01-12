# wedding-book

Virtual Environment commands:
    start:  .\.venv\Scripts\activate.bat
    stop:   deactivate

# Django
    ## Log In
    User:admin
    Password: admin

    ## Start
    python manage.py runserver
    
    ## Migration
    Models can continously be adjusted but have to be migrated afterwards.
    If you for example want to add another attribute, insert it into the according model.
    After that you have to call two commands:

    python manage.py migrate
    python manage.py makemigrations webui (>According App<)

