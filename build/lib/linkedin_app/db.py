from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_


db = SQLAlchemy()

class UserProfile(db.Model):
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
        return UserProfile.query.get(profile_id)

    @staticmethod
    def delete_profile(profile_id):
        print 'Deleting {0}'.format(profile_id)
        profile = UserProfile.query.get(profile_id)

        db.session.delete(profile)
        db.session.commit()

        return profile

    @staticmethod
    def profile_exists(profile):
        existing_profile = UserProfile.query.filter(and_(UserProfile.firstName == profile.firstName
                                              ,UserProfile.lastName == profile.lastName)).first()

        return existing_profile is not None

    @staticmethod
    def search_simple(search_str):
        words = search_str.split()
        all_results = []

        for word in words:
            results = UserProfile.query.filter(UserProfile.firstName.contains(word)
                                               | UserProfile.lastName.contains(word)).all()

            for result in results:
                if result not in all_results:
                    all_results.append(result)

        return all_results

    @staticmethod
    def search(search_obj):

        finalQuery = None
        for attribute, value in search_obj.iteritems():
            print attribute, value  # example usage
            query = None
            if attribute == "firstName":
                query = UserProfile.firstName.contains(value)
            elif attribute == "lastName":
                query = UserProfile.lastName.contains(value)
            elif attribute == "bio":
                query = UserProfile.bio.contains(value)
            else:
                continue

            if finalQuery is None:
                finalQuery = query
            else:
                finalQuery = finalQuery & query

        results = UserProfile.query.filter(finalQuery).all()

        return results
