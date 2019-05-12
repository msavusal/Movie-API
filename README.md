# PWP SPRING 2019
# Movie API
# Group information
* Student 1. Jaakko Seppänen jaakko.seppanen@student.oulu.fi
* Student 2. Markus Savusalo markus.savusalo@windowslive.com
* Student 3. Tuomas Savusalo tuomas.savusalo@windowslive.com


## All dependencies (external libraries) and how to install them
This project uses Django and Django REST Framework along with drf-hal-json.
To install use *requirements.txt*:
```
pip install -r requirements.txt
```
*Alternatively* you can manually install the required packages:
```
pip install django==2.1.5
pip install djangorestframework==3.9.1
pip install drf-nested-fields==0.9.4
pip install drf-hal-json==0.9.1
pip install coverage==4.5.3
pip install django-nose==1.4.6
```

## How to run the server
Command to start the server:
```python
python manage.py runserver
```
This starts a local server **localhost:8000**

## Database and version utilized
Name of the database file is *db.sqlite3* and can be found in the root of the project.

Database used is SQLite. In this project we use sqlite3 module, since it provides a SQL interface compliant with the DB-API 2.0 specification as described by [PEP 249](https://www.python.org/dev/peps/pep-0249/).

## How to setup the database framework and external libraries
To set up the database for the first time **two** steps are required (in the main Movie-API folder):
```python
python manage.py makemigrations
```
Which is responsible for creating new migrations based on the changes made to the ORM models.
```python
python manage.py migrate
```
Which is responsible for applying and unapplying migrations, aka. the actual changes to the DB.

To run the server and browse through the database via browser run command:
```python
python manage.py runserver
```
This starts a local server **localhost:8000**

## How to setup and populate the database (not necessary)
To populate database run the following command (in the main Movie-API folder):
```python
python manage.py loaddata db.json
```
This uses a json dump file to populate the database. Howerver, an already populated database file is already included in the repository.

## How to run the tests
To run the test run the following command (in the main Movie-API folder):
```python
python manage.py test
```
This will use **coverage** to create a cover html report in the following folder:
```
Movie-API  
└───cover
    └───index.html
```

## Main files
Location of ORM models (code) in project:
```
Movie-API  
└───movieapi
    └───app
        │   models.py
```        

All other main files containing our code:
```
Movie-API  
└───movieapi
    │   settings.py
    │   urls.py
    └───app
        │   models.py
        │   permissions.py
        │   serializers.py
        │   tests.py
        │   views.py
```    
