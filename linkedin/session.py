import uuid
from flask import session
from datetime import timedelta

# hard coded admin users
admin_users = ['anna', 'guy', 'tom', 'dolev']
session_timeout = 1


class Session:
    def __init__(self, cache):
        self.cache = cache

    def login(self, username):
        user_id = str(uuid.uuid4())
        self.cache.set(user_id, username, timeout=session_timeout)

        session['username'] = username
        session['user_id'] = user_id
        session['logged_in'] = True

    def logout(self):

        if 'user_id' in session:
            self.cache.delete(session['user_id'])

        # remove the username from the session if it's there
        session.pop('logged_in', None)
        session.pop('username', None)
        session.pop('user_id', None)

    def get_user_id(self):
        if 'user_id' in session:
            return session['user_id']
        else:
            return ''

    def get_username(self):

        if 'user_id' in session:
            return self.cache.get(session['user_id'])
        else:
            return ''

    def update_ttl(self, app):
        session.permanent = True

        app.permanent_session_lifetime = timedelta(minutes=session_timeout)

        if 'user_id' in session:
            self.cache.set(session['user_id'], session['username'], timeout=session_timeout * 60)

    def check_admin_permissions(self):
        if 'user_id' in session:
            username = self.cache.get(session['user_id'])
            return username in admin_users

        return False
