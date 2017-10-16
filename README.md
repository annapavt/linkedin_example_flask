      / My LinkedIn App /

This is a simple linkeidn like app that supports the following features:

- add new user profile with first name, last name , email address and a short biography section.
- search - supports basic string search that searches the first and last name field
           supports JSON format that allows complex queries on several fields.
           For example: {"firstName":"John","lastName":"Doe"}

Installation
=================

To install the app on your machine:

virtualenv venv
source venv/bin/activate

pip install -r requirements.txt

Install redis on mac:

brew install redis


Execution
=================

First start the database and generate some dummy data:

 python -m linkedin.init_db

Start redis for caching :
redis-server /usr/local/etc/redis.conf


To run the app on 2 gunicorn servers:

unicorn "linkedin.app:create_app()" -b 0.0.0.0:8000 -w 2

Now go to: http://localhost:8000

Voila!


Tests
=================
The app is tested using pytest.

To run the tests:

    py.test tests


Locust scale and performance tests
===================================

locust -f tests/locust_test.py --host=http://localhost:8000

