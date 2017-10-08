from flask import Flask, render_template, request, session, redirect, url_for, flash
import json
from datetime import timedelta
from db import db, UserProfile
from users import Users

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/my.db'
    db.init_app(app)

    users = Users()

    # set session timeout to be 30 seconds of inactivity
    @app.before_request
    def make_session_permanent():
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=5)


    @app.route('/')
    def index():
        return render_template('index.html')


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']

            user_id = users.add_user(username)

            session['username'] = username
            session['user_id'] = user_id
            session['logged_in'] = True

            return redirect(url_for('index'))

        return render_template('login.html')


    @app.route('/logout')
    def logout():
        # remove the username from the session if it's there
        session.pop('logged_in', None)
        session.pop('username', None)
        session.pop('user_id', None)


        return redirect(url_for('index'))

    @app.route('/add_profile',methods=['GET','POST'])
    def add_profile():
        if request.method == 'POST':

            first_name = request.form['firstName']
            last_name = request.form['lastName']
            email = request.form['email']
            bio = request.form['bio']

            print 'Adding {0} {1} {2}'.format(first_name,last_name,email)
            new_profile = UserProfile(firstName=first_name, lastName=last_name, email=email, bio=bio)

            if UserProfile.profile_exists(new_profile):
                flash("Profile with same first and last name already exists")
                return redirect(url_for('add_profile'))

            else:
                UserProfile.add_profile(new_profile)
                flash("Profile added successfully")

                return show_profile(id=new_profile.id)
        else:
            return render_template('add_profile.html')


    @app.route('/show_profile/<id>')
    def show_profile(id=None):
        if id:
            user_profile = UserProfile.query.get(id)
            return render_template('show_profile.html', profile=user_profile)
        else:
            return 'Profile not found'


    @app.route('/delete_profile/<id>', methods=['POST'])
    def delete_profile(id=None):

        # check is user is an admin
        if 'user_id' in session and users.check_delete_permissions(session['user_id']):

            profile = UserProfile.delete_profile(id)

            flash("Profile for {0} {1} was succesfully deleted.".format(profile.firstName, profile.lastName))
            return redirect(url_for('index'))

        else:
            flash("You don't have permission to delete profiles")
            return redirect(url_for('show_profile', id=id))


    @app.route('/search', methods=['GET', 'POST'])
    def search():
        if request.method == 'POST':
            search_str = request.form['search']

            try:
                search_obj = json.loads(search_str)
                all_results = UserProfile.search(search_obj)

            except ValueError, e:
                all_results = UserProfile.search_simple(search_str)

            return render_template('search_results.html', results=all_results)
        else:
            return render_template('search.html')


    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

    return app

# if __name__ == "__main__":
#     create_app().run()
