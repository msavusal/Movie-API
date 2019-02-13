# PWP SPRING 2019
# Movie API
# Group information
* Student 1. Jaakko Seppännen jaakko.seppanen@student.oulu.fi
* Student 2. Markus Savusalo markus.savusalo@windowslive.com
* Student 3. Tuomas Savusalo tuomas.savusalo@windowslive.com


## All dependencies (external libraries) and how to install them
This project uses Django and Django REST Framework.
To install use *requirements.txt*:
```
pip install -r requirements.txt
```
*Alternatively* you can manually install the two packages:
```
pip install django==2.1.5
pip install djangorestframework==3.9.1
```

## Database and version utilized
Database used is SQLite. In this project we use sqlite3 module, since it provides a SQL interface compliant with the DB-API 2.0 specification as described by [PEP 249](https://www.python.org/dev/peps/pep-0249/).
## Instructions how to setup the database framework and external libraries
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

## Instructions on how to setup and populate the database.
To populate database run the following command (in the main Movie-API folder):
```python
python manage.py loaddata db.json
```
This uses a json dump file to populate the database. Howerver, an already populated database file is already included in the repository.
## Instruction on how to run the tests on the database.
To run the test run the following command (in the main Movie-API folder):
```python
python manage.py test
```
## Main files
Location of ORM models (code) in project:
```
Movie-API  
└───movieapi
    └───app
        │   models.py
```        

All other main files containing our code (updated 13.02.):
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
