# ASSESSMENT

## Description

You are working for a small bank that is willing to setup a homebanking system to improve their competitiveness and reduce their costs. Their database is located on the cloud and contains the following information :

- Account type (Credit card, etc)
- Account number
- Current account balance
- Client’s name
- Client’s address
- Client’s first name
- Client’s date of birth

Based on this database, the company wants to build a cross device system, accessible from tablets, smartphones, etc.  

You are aware that a QA department will review the quality of your work.



## Task #1 – Web server

Write a python code snippet of a RESTful API that exposes the database content.



## Task #2 – Logging Component

For traceability reason, it is required to log all actions in a separate component (and separate database). Using ZeroMQ, connect the web server to a component that will simply collect all actions in a log file (can be a basic text file, structure is not very important).



## Guidelines

- The programming language for the RESTful API must be Python
- Keep good development practices in mind
- You can choose the database (SQL-based: mysql, pgsql, jackrabbit, CSV, oracle, ... ; NoSQL : mongoDB, couchDB, XML, Cassandra...)
- Provide a simple CRUD
- Send the code at least 24h before the interview


***


# SOLUTION

## Task #1
### Modelisation
The solution is built over the [Django](https://www.djangoproject.com/) framework.  
The emerging classes are `Address`, `Client` and `Account`.  Note that for account numbers, the [IBAN format](http://en.wikipedia.org/wiki/International_Bank_Account_Number) has been chosen.  
The modelisation of the concepts can be found in `models.py`.  

### REST API
The REST API is exposed thanks to [Tastypie](https://django-tastypie.readthedocs.org/en/latest/) and its doc automatically built with [Swagger](https://pypi.python.org/pypi/django-tastypie-swagger).  Swagger makes it especially easy to test either by QA dpt or other devs, for instance.

### Database
To keep things simple, this POC uses a simple sqlite database.  Thanks to Django, it can be easily modified (see the Django doc, [Connecting to the database](https://docs.djangoproject.com/en/dev/ref/databases/#connecting-to-the-database)).  
Some fixtures are shipped with the project, so the features can be tested immediately.


## Task #2
It's not necessary to [write a new logging handler](http://stackoverflow.com/q/3118059/1030960): ZMQ already provides one using the PUB/SUB pattern (see [Asynchronous Logging via PyZMQ](http://zeromq.github.io/pyzmq/logging.html)).  The logger is plugged in the API by overriding the `tastypie.resources.ModelResource.dispatch()` method (see the `CustomModelResource` class).


***


# INSTALL and RUN

The following steps assume you have Python and [pip](https://pypi.python.org/pypi/pip) up and running. 

    $ git clone git@github.com:abourguignon/cluepoc.git
    $ cd cluepoc
    $ pip install -r requirements.txt  # install Python depedencies
    $ ./homebanking/manage.py migrate  # create the database (the default is sqlite, but it can be changed in settings.py)
    $ ./homebanking/manage.py createsuperuser  # create a Django user; these credentials are necessary to access the admin panel and the API
    $ ./homebanking/manage.py loaddata demo_data  # load the fixtures

All set: let's run it.

    $ ./homebanking/manage.py runserver  # launch the django project, accessible at http://localhost:8000
    $ ./zmqlogger/zmqlogger_sub.py  # launch the zmq logger (listener)

The API is exposed at `http://localhost:8000/webservice/api/v0/`.  
It's possible to directly play with it through Swagger (have a look at `http://localhost:8000/webservice/api/v0/doc/`) and see what the logger does (with `tail -f zmqlogger/access.log`, for instance, but it also prints directly in the terminal).  
An admin panel is also available (`http://localhost:8000/admin/`) to modify data through a web interface.
