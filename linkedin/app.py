from flask import Flask, render_template, request, redirect, url_for, flash
import json
from db import SqlDB
from flask_caching import Cache
from session import Session


def create_app(config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/my.db'
    app.config['DEBUG'] = True
    app.config.update(config or {})

    if 'db' in app.config:
        db = app.config['db']
    else:
        db = SqlDB()

    db.init_app(app)

    if config and 'cache' in config:
        cache = config['cache']
    else:
        cache = Cache(config={'CACHE_TYPE': 'redis',
                          'CACHE_THRESHOLD': 100})
    cache.init_app(app)

    session = Session(cache)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']

            session.login(username)

            return redirect(url_for('index'))

        return render_template('login.html')

    @app.route('/logout')
    def logout():

        session.logout()
        return redirect(url_for('index'))

    @app.route('/add_profile', methods=['GET', 'POST'])
    def add_profile():
        if request.method == 'POST':

            first_name = request.form['firstName']
            last_name = request.form['lastName']
            email = request.form['email']
            bio = request.form['bio']

            new_profile = db.create_profile(first_name, last_name, bio, email)

            if db.profile_exists(new_profile):
                flash("Profile with same first and last name already exists")
                return redirect(url_for('add_profile'))

            else:
                db.add_profile(new_profile)
                cache.delete_memoized(search_db)

                flash("Profile added successfully")

                return show_profile(id=new_profile.id)
        else:
            return render_template('add_profile.html')

    @app.route('/show_profile/<id>')
    def show_profile(id=None):
        if id:
            user_profile = db.get_profile(id)
            return render_template('show_profile.html', profile=user_profile)
        else:
            return 'Profile not found'

    @app.route('/delete_profile/<id>', methods=['POST'])
    def delete_profile(id=None):

        # check is user is an admin
        if session.check_admin_permissions():

            profile = db.delete_profile(id)

            cache.delete_memoized(search_db)
            flash("Profile for {0} {1} was succesfully deleted.".format(profile.firstName, profile.lastName))
            return redirect(url_for('index'))

        else:
            flash("You don't have permission to delete profile {0} ".format(session.get_username()))

            return redirect(url_for('show_profile', id=id))

    @app.route('/search', methods=['GET', 'POST'])
    def search():
        if request.method == 'POST':
            search_str = request.form['search']

            results = search_db(search_str)

            if results is None:
                results = []
            return render_template('search.html', results=results, search_str=search_str)
        else:
            return render_template('search.html', search_str="John")

    @cache.memoize()
    def search_db(search_str):
        try:
            search_obj = json.loads(search_str)
            return db.search(search_obj)

        except ValueError, e:
            return db.search_simple(search_str)

    @app.before_request
    def make_session_permanent():
        # set session timeout to be 60 seconds of inactivity
        session.update_ttl(app)

    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

    return app


if __name__ == "__main__":
    create_app().run()
