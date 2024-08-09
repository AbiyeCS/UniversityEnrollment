to  virtual ennviorment create env 
 cd project 
 virtualenv venv

 On Windows:

.\venv\Scripts\activate
On macOS and Linux:


source venv/bin/activate

to install requirements
pip install -r requirements.txt

to migrate database
python manage.py migrate

to create superuser
python manage.py createsuperuser "and then follow the inputs "

to run the app
python manage.py runserver 8000

For Seeding Data
For running new changes of AI
pip install -r requirements.txt
if redis is not install through pip,run
    brew install redis
    python manage.py migrate
    python manage.py seed_student
    python manage.py seed_application
    python manage.py

For Running the Server your need 3 terminal
first terminal:
    python manage.py runserver
second terminal:
    celery -A sapms worker --loglevel=info
3rd terminal:
    rm celerybeat-schedule
    celery -A sapms beat --loglevel=info

For Demo
login as admin
add weight's to all universities to see the recommendations
For pre-training -> /admin_dashboard/model-training/
for seeing and deleting training data -> /admin_dashboard/training-data/
for seeing recommendations -> /admin_dashboard/all_recommendations/

For you to see recommendations you have to set the initial weightage for a university in http://127.0.0.1:8000/admin/university_panel/universityaiweight/ 

