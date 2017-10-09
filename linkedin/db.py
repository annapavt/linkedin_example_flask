from abc import abstractmethod, ABCMeta

from sqlalchemy import and_

from linkedin.model import UserProfileTable


class DB:
    __metaclass__ = ABCMeta

    @abstractmethod
    def init_app(self, app):
        pass

    @abstractmethod
    def reset(self, app):
        pass

    @abstractmethod
    def create_profile(self, first_name, last_name, email, bio):
        pass

    @abstractmethod
    def add_profile(self, new_profile):
        pass

    @abstractmethod
    def get_profile(self, profile_id):
        pass

    @abstractmethod
    def delete_profile(self, profile_id):
        pass

    @abstractmethod
    def profile_exists(self, profile):
        pass

    @abstractmethod
    def search_simple(self, search_str):
        pass

    @abstractmethod
    def search(self, search_obj):
        pass


class FakeDB(DB):
    def search(self, search_obj):
        # print 'search {0}'.format(search_obj)
        return []

    def init_app(self, app):
        print 'init_app'

    def create_profile(self, first_name, last_name, email, bio):
        return UserProfileTable(id=1, firstName=first_name, lastName=last_name, email=email, bio=bio)

    def reset(self, app):
        print 'reset'

    def search_simple(self, search_str):
        # print 'search_simple {0}'.format(search_str)
        return []

    def profile_exists(self, profile):
        # print 'profile_exists {0}'.format(profile)
        return False

    def delete_profile(self, profile_id):
        print 'delete_profile'.format(profile_id)

    def get_profile(self, profile_id):
        # print 'get_profile {0}'.format(profile_id)
        return self.create_profile("John", "Doe", "sdafds@gmail.com", "bla bla bla")

    def add_profile(self, new_profile):
        print 'add_profile {0}'.format(new_profile)

from settings import db

class SqlDB(DB):

    def init_app(self, app):
        db.init_app(app)

    def reset(self, app):
        with app.app_context():
            db.drop_all()
            db.create_all()

    def create_profile(self, first_name, last_name, email, bio):
        return UserProfileTable(firstName=first_name, lastName=last_name, email=email, bio=bio)

    def add_profile(self, new_profile):
        db.session.add(new_profile)
        db.session.commit()

    def get_profile(self, profile_id):
        return UserProfileTable.query.get(profile_id)

    def delete_profile(self, profile_id):
        profile = UserProfileTable.query.get(profile_id)

        session = db.object_session(profile)
        session.delete(profile)
        session.commit()

        return profile

    def profile_exists(self, profile):
        existing_profile = UserProfileTable.query.filter(and_(UserProfileTable.firstName == profile.firstName,
                                                              UserProfileTable.lastName == profile.lastName)).first()

        return existing_profile is not None

    def search_simple(self, search_str):
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

    def search(self, search_obj):

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

        if final_query is None:
            results = UserProfileTable.query.all()
        else:
            results = UserProfileTable.query.filter(final_query).all()


        return results
