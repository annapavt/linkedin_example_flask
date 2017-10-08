from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from loremipsum import generate_paragraph

import names
from app import UserProfile

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/my.db'
db = SQLAlchemy(app)


for i in range(0,100):
    p = UserProfile(firstName=names.get_first_name(), lastName=names.get_last_name())
    p.email = '{0}_{1}@gmail.com'.format(p.firstName,p.lastName).lower()

    sentences_count, words_count, paragraph = generate_paragraph()
    p.bio = paragraph[0:300]
    db.session.add(p)
    db.session.commit()