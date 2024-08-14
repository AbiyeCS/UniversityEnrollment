# How To Run #

## Prerequisites ## 
Before running the project, ensure you have the following installed:
- Download Python - https://www.python.org/downloads/release/python-3123/
- Clone Repository - https://github.com/AbiyeCS/UniversityEnrollment
- Install Docker - https://www.docker.com/products/docker-desktop/ 

## Build docker containers ##
    docker compose -f ./docker-compose.yml up -d
#### Run this command in the UniversityEnrollment directory

## Seeding data ##
- In docker click on sapms_django container
- click on the Exec tab 
- Run the following commands within this tab
        


    python manage.py seed_student
#### Note: This will create an admin user with "username=admin;password=password123" and 50 students "username=student_1;password=password123"
    python manage.py seed_university
#### Note: This will create dummy 10 universities "username=dummyuser0:password=dummyuserpassword
    python manage.py seed_application 
#### Note: This will create 500 applications
