from linkedin.app import create_app
from loremipsum import generate_paragraph
import names
from linkedin.model import UserProfileTable
from linkedin import model
import sys
from db import SqlDB


def init_db(config=None, profiles_num=0):
    app = create_app(config)
    db = SqlDB()
    db.init_app(app)

    with app.app_context():
        model.db.drop_all()
        model.db.create_all()

    for i in range(0, profiles_num):
        p = UserProfileTable(firstName=names.get_first_name(), lastName=names.get_last_name())
        p.email = '{0}_{1}@gmail.com'.format(p.firstName, p.lastName).lower()

        sentences_count, words_count, paragraph = generate_paragraph()
        p.bio = paragraph[0:300]

        with app.app_context():
            db.add_profile(p)

    print 'Created database with {0} profiles. '.format(profiles_num)


if __name__ == "__main__":
    init_db(profiles_num=int(sys.argv[1]))
