from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Invitees(db.Model):
    __tablename__ = "invitees"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(10))
    last_name = db.Column(db.String(10))
    location = db.Column(db.String(20))

    def __init__(self, first_name, last_name, location):
        self.first_name = first_name
        self.last_name = last_name
        self.location = location

    def __repr__(self):
        return f"{self.first_name}:{self.last_name}:{self.location}"

