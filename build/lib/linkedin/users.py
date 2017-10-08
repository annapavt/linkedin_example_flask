import uuid


class Users:
    # hard coded admin users
    admin_users = ['anna', 'guy', 'tom', 'dolev']

    user_ids = {}

    def add_user(self, username):
        user_id = uuid.uuid4()
        self.user_ids[user_id] = username
        return user_id

    def check_delete_permissions(self, user_id):
        if user_id not in self.user_ids.keys():
            return False

        username = self.user_ids[user_id]

        return username in self.admin_users
