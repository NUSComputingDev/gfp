# NUS SoC GFP

This is a repository for the NUS School of Computing Graduate Farewell Party (GFP) system

## Installation

### Requirements
* Python 3 (2.7 is OK, but may cause problems)
* Django 1.9.2

### Development
Just run the following commands
```bash
$ manage.py makemigrations
$ manage.py migrate
$ manage.py runserver
```

Your website will now be running on [localhost:8000](http://127.0.0.1:8000/)

### Production
As the code is not yet production-ready, there are currently no instructions to set up a production-ready server.
