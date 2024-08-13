# How To Run #

## Prerequisites ## 
Before running the project, ensure you have the following installed: 
- Python3: You can verify the installation by running $python3 --version 
- Download PyCharm - https://www.jetbrains.com/pycharm/download/?section=mac
- Download Python3 - https://www.python.org/downloads/release/python-3123/
- Download Homebrew - https://docs.brew.sh/Installation
- Clone Repository - https://github.com/AbiyeCS/UniversityEnrollment

## To create virtual environment ###
#### When opening pycharm it should present you the option to configure virtual env automatically, if not use commands below ####

### On Windows: ###
    python3 -m venv venv
    .\venv\Scripts\activate 

### On macOS and Linux: ###
    python3 -m venv venv
    source venv/bin/activate

## Installing Requirements/Dependencies ##
    pip install -r requirements.txt
    pip install Django
    pip install django-ckeditor
    pip install joblib
    pip install pandas
    pip install scikit-learn
    pip install celery
    python -m pip install Pillow
    brew install redis

## Migrate database ##
    python manage.py migrate

## Create superuser / Admin ##
    python manage.py createsuperuser

## For Seeding Data ##
    python manage.py seed_student
    python manage.py seed_university
    python manage.py seed_application

## For running the application, you need 3 terminals ##
### First terminal: ###
    python manage.py runserver
### Second terminal: ###
    brew services start redis
    celery -A sapms worker --loglevel=info

#### Note: Initially errors will show within the second terminal due to the training set being empty. This will go once training data is collected from application or dataset is added. ####
### Third terminal: ###
    rm celerybeat-schedule
    celery -A sapms beat --loglevel=info

#### Note: You can also manually remove the celerybeat-schedule by deleting the file directly from the home directory if it exists, if it doesn't can go straight to the second command of the two ####

## Demo - Upon initially starting application for the first time no recommendations will show ##
- Login as admin
- Add weights to all universities to see the recommendations - http://127.0.0.1:8000/admin/university_panel/universityaiweight/
- Press Add University weight button in top right corner 
- Select the university weighting you want to change from the dropdown menu 
- The total weightage of GPA, Extracurricular and sport should equal 100 e.g GPA = 30, Extracurricular = 30 and Sports = 40. 
- Once weights are added go to http://127.0.0.1:8000/admin_dashboard/all_recommendations/
- Click Refresh Recommendation button and recommendations will now show

## To add a dataset/training data ##
- Go to http://127.0.0.1:8000/admin_dashboard/model-training/
- Choose file, dataset is in UniversityEnrollment/media/training_files
- Click upload
- If you get an error run “redis-server” and ensure that is running, then restart both of the celery terminals - If it’s still not working it may be because Firewall is blocking connection to Redis, you have to configure your firewall to Allow connections to the Redis server on the necessary port (6379)

## To access database in PyCharm ## 
- Double click db.sqlite3 in the home directory 
- Click apply 
- Click Ok 
- Then you should now see the database entries in the database tab to the right of this window (If)