# How To Run #

## Prerequisites ## 
Before running the project, ensure you have the following installed: 
- Python3: You can verify the installation by running $python3—version command

## To create virtual environment ###
    cd project 
    virtualenv venv

### On Windows: ###
    .\venv\Scripts\activate 

### On macOS and Linux: ###
    source venv/bin/activate

## Installing Requirements/Dependencies ##
    pip install -r requirements.txt

## Migrate database ##
    python manage.py migrate

## Create superuser / Admin ##
    python manage.py createsuperuser "and then follow the inputs"

to run the app
python manage.py runserver 8000

#### Note: if redis is not install through pip, run brew install redis ####

## For Seeding Data ##
    python manage.py migrate
    python manage.py seed_student
    python manage.py seed_university
    python manage.py seed_application
    python manage.py

## For running the application, you need 3 terminals ##
### first terminal: ###
    python manage.py runserver
### second terminal: ###
    celery -A sapms worker --loglevel=info
### third terminal: ###
    rm celerybeat-schedule
    celery -A sapms beat --loglevel=info

#### Note: You can also manually remove the celerybeat-schedule by deleting the file directly from the home directory ####

## Demo ##
- Login as admin
- Add weight's to all universities to see the recommendations - http://127.0.0.1:8000/admin/university_panel/universityaiweight/
- For pre-training -> /admin_dashboard/model-training/
- for seeing and deleting training data -> /admin_dashboard/training-data/
- for seeing recommendations -> /admin_dashboard/all_recommendations/


## To access database in PyCharm ## 
- Double click db.sqlite3 in the home directory 
- Click apply 
- Click Ok 
- Then you should now see the database entries in the database tab to the right of this window (If)