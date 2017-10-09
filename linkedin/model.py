from settings import db

class UserProfileTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(80), unique=False, nullable=False)
    lastName = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    bio = db.Column(db.String(300), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id
