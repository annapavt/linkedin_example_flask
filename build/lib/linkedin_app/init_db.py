from linkedin.app import create_app
from linkedin.app import db

app = create_app()

with app.app_context():
    db.create_all()


