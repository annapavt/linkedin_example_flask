from linkedin.app import create_app
from linkedin.app import db
from loremipsum import generate_paragraph
import names
from db import UserProfile


def init_db(config=None):
    app = create_app(config)

    with app.app_context():
        db.drop_all()
        db.create_all()

    for i in range(0, 100):
        p = UserProfile(firstName=names.get_first_name(), lastName=names.get_last_name())
        p.email = '{0}_{1}@gmail.com'.format(p.firstName, p.lastName).lower()

        sentences_count, words_count, paragraph = generate_paragraph()
        p.bio = paragraph[0:300]

        with app.app_context():
            db.session.add(p)
            db.session.commit()


if __name__ == "__main__":
    init_db()
