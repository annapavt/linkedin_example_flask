      / My LinkedIn App /

This is a simple linkeidn like app that supports the following features:

- add new user profile with first name, last name , email address and a short biography section.
- search - supports basic string search that searches the first and last name field
           supports JSON format that allows complex queries on several fields.
           For example: {"firstName":"John","lastName":"Doe"}

Installation
=================

To install the app on your machine:

pip install -r requirements.txt

Install redis on mac:

brew install redis

Execution
=================



First start the database and generate some dummy data:

 python -m linkedin.init_db

Start redis for caching :
redis-server /usr/local/etc/redis.conf

To run the app:

 python -m linkedin.app


Now go to: http://localhost:5000

Voila!


Tests
=================
The app is tested using pytest.

To run the tests:

    py.test tests