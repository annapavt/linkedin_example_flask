from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_

db = SQLAlchemy()


class UserProfileTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(80), unique=False, nullable=False)
    lastName = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    bio = db.Column(db.String(300), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

    @staticmethod
    def add_profile(new_profile):
        db.session.add(new_profile)
        db.session.commit()

    @staticmethod
    def get_profile(profile_id):
        return UserProfileTable.query.get(profile_id)

    @staticmethod
    def delete_profile(profile_id):
        print 'Deleting {0}'.format(profile_id)
        profile = UserProfileTable.query.get(profile_id)

        db.session.delete(profile)
        db.session.commit()

        return profile

    @staticmethod
    def profile_exists(profile):
        existing_profile = UserProfileTable.query.filter(and_(UserProfileTable.firstName == profile.firstName,
                                                              UserProfileTable.lastName == profile.lastName)).first()

        return existing_profile is not None

    @staticmethod
    def search_simple(search_str):
        if len(search_str) == 0:
            return UserProfileTable.query.all()

        words = search_str.split()
        all_results = []

        for word in words:
            results = UserProfileTable.query.filter(UserProfileTable.firstName.contains(word)
                                                    | UserProfileTable.lastName.contains(word)).all()

            for result in results:
                if result not in all_results:
                    all_results.append(result)

        return all_results

    @staticmethod
    def search(search_obj):

        final_query = None
        for attribute, value in search_obj.iteritems():
            query = None
            if attribute == "firstName":
                query = UserProfileTable.firstName.contains(value)
            elif attribute == "lastName":
                query = UserProfileTable.lastName.contains(value)
            elif attribute == "bio":
                query = UserProfileTable.bio.contains(value)
            else:
                continue

            if final_query is None:
                final_query = query
            else:
                final_query = final_query & query

        if final_query:
            results = UserProfileTable.query.filter(final_query).all()
        else:
            results = UserProfileTable.query.all()

        return results
